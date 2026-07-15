import asyncio

from datetime import datetime, UTC

from models.python.conversation.content_block import ContentBlock
from models.python.conversation.converstation_message import ConversationMessage
from models.python.awareness.processing_context import ProcessingContext

from nervous_system.signal_bus.schemas.tool_schemas import TOOL_SCHEMAS

from infrastructure.containers.container import Container



MAX_TOOL_ROUNDS = 5


# -------------- INITS ----------------
class Orchestrator:

    def __init__(self, container: Container):
        self.container = container

        self.advisor = container.advisor_service
        self.memory = container.memory_service
        self.conversation = container.conversation_service
        self.tool_executor = container.tool_executor

        self.state_manager = container.state_manager
        self.graph_memory = container.graph_memory_service

        self.identity = container.identity_service
        self.goal_manager = container.goal_manager
        self.self_model = container.self_model_service

        self.episode_service = container.episode_service
        self.memory_gate = container.memory_gate

        self.cognition_extractor = container.cognition_extractor

        self.cache_service = container.cache_service
        self.context_builder = container.context_builder


    # --------------- CORE ----------------
    async def process(self, session_id: str, msg: str):
        
        self.cache_service.ensure_session(session_id)
        self.cache_service.clear_message()

        ctx = ProcessingContext(
            session_id=session_id,
            user_message=msg
        )

        await self._store_user_message(ctx)
        await self._build_context(ctx)
        await self._reason(ctx)
        await self._store_response(ctx)

        asyncio.create_task(self._learn(ctx))
        
        return ctx.answer
    


    # -------- ASYNCED PROCESSING ---------
    async def _learn(self, ctx):
        try: 
            await self._extract_memories(ctx)
            await self.cache_service.refresh_boot()

        except Exception:
            print("[ERROR][ORC] Learning pipline failed")


    # ------------- BUILDERS ---------------
    async def _store_user_message(self, ctx: ProcessingContext):
        ctx.user_message_id = await self.conversation.store_message(
            session_id=ctx.session_id,
            message=ConversationMessage(
                role="user",
                content=[
                    ContentBlock(
                        type="text",
                        content=ctx.user_message,
                    )
                ]
            ),
        )


    async def _build_context(self, ctx: ProcessingContext):
        ctx.cognitive_context = await self.context_builder.build(
            session_id=ctx.session_id, 
            query=ctx.user_message, 
            cache=self.cache_service.cache
        )

        ctx.prompt = ctx.cognitive_context.render()

        self.cache_service.cache.message.prompt = ctx.prompt

        # BUILD INITIAL MESSAGES
        ctx.llm_messages = [
            ConversationMessage(
                role="system",
                content=[
                    ContentBlock(
                        type="text",
                        content=ctx.prompt,
                    ),
                ]
            ),
            ConversationMessage(
                role="user",
                content=[
                    ContentBlock(
                        type="text",
                        content=ctx.user_message,
                    )
                ]
            )
        ]


    async def _reason(self, ctx: ProcessingContext):
        for _ in range(MAX_TOOL_ROUNDS):
            print(f"[DEBUG][ORCHESTRATOR][{datetime.now():%X}] Prompt sent to API: {ctx.llm_messages}")

            response = await self.advisor.ask(
                task="reasoning", 
                messages=ctx.llm_messages,
            )

            print(f"[DEBUG][GIDEON][ORCHESTRATOR][{datetime.now():%X}] {response}")

            if response is None:
                raise RuntimeError("AdvisorService returned None. Check Advisor Logs")

            gideon_msg = ConversationMessage(
                role="gideon",
                content=[
                    ContentBlock(
                        type="text",
                        content=response.content,
                    )
                ],
            )

            if response.tool_calls:
                gideon_msg.content.append(
                    ContentBlock(
                        type="text",
                        content=response.tool_calls
                    )
                )


                ctx.llm_messages.append(gideon_msg)

                ctx.tool_results = await self.tool_executor.execute(tool_calls=response.tool_calls)
                
                ctx.llm_messages.extend(ctx.tool_results)

                continue
        
            ctx.answer = response.content

            return

        # Safe fallback
        ctx.answer = "Max tool execution rounds reached."


    async def _store_response(self, ctx: ProcessingContext):
        await self.conversation.store_message(
            session_id=ctx.session_id,
            message=ConversationMessage(
                role="gideon",
                content=[
                    ContentBlock(
                        type="text",
                        content=ctx.answer,
                    )
                ]
            ),
        )


    # pure learning phase
    async def _extract_memories(self, ctx: ProcessingContext):
        await self.episode_service.add_interaction(
            session_id=ctx.session_id, 
            user_msg=ctx.user_message, 
            gideon_msg=ctx.answer
        )

        await self.episode_service.schedule_finalize(ctx.session_id)

        if self.memory_gate.should_extract(user_msg=ctx.user_message, gideon_msg=ctx.answer):
            await self.cognition_extractor.extract(
                user_msg=ctx.user_message, 
                gideon_response=ctx.answer,

                message_id=ctx.user_message_id, 
                episode_id=ctx.episode_id,
                session_id=ctx.session_id,

                context=ctx,
            )