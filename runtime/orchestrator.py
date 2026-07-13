from datetime import datetime, UTC

from models.python.conversation.content_block import ContentBlock
from models.python.conversation.converstation_message import ConversationMessage

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
        self.memory_extractor = container.memory_extractor

        self.state_extractor = container.state_extractor

        self.cache_service = container.cache_service
        self.context_builder = container.context_builder


    # --------------- CORE ----------------
    async def process(self, session_id: str, msg: str):

        # STEP 0: CLEAR OLD CACHE DATA
        session_cache = self.cache_service.session(session_id)
        self.cache_service.clear_message()
        

        # STEP 1: STORE USER MSG
        user_message_id = await self.conversation.store_message(
            session_id=session_id,
            message=ConversationMessage(
                role="user",
                content=[
                    ContentBlock(
                        type="text",
                        content=msg,
                    )
                ]
            ),
        )

        # STEP 2: BUILD CONTEXT
        cognitive_context = await self.context_builder.build(session_id=session_id, query=msg, cache=self.cache_service.cache)

        self.cache_service.cache.message.prompt = cognitive_context.render()

        # STEP 3: BUILD INITIAL MESSAGES
        messages = [
            ConversationMessage(
                role="system",
                content=[
                    ContentBlock(
                        type="text",
                        content=cognitive_context.render(),
                    ),
                ]
            ),
            ConversationMessage(
                role="user",
                content=[
                    ContentBlock(
                        type="text",
                        content=msg,
                    )
                ]
            )
        ]

        # STEP 3: LLM + TOOL LOOP
        tool_results = []

        for _ in range(MAX_TOOL_ROUNDS):
            print(f"[DEBUG][ORCHESTRATOR][{datetime.now():%X}] Prompt sent to API: {messages}")

            response = await self.advisor.ask(
                task="reasoning", 
                messages=messages,
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
                tool_call = ContentBlock(
                    type="text",
                    content=response.tool_calls
                )

                gideon_msg.content.append(tool_call)

            messages.append(gideon_msg)

            if not response.tool_calls:
                answer = response.content
                break

            results = await self.tool_executor.execute(tool_calls=response.tool_calls)
            
            tool_results.extend(results)
            messages.extend(results)

        # Safe fallback
        else:
            answer = "Max tool execution rounds reached."

        # STEP 4: STORE RESPONSE
        await self.conversation.store_message(
            session_id=session_id,
            message=ConversationMessage(
                role="gideon",
                content=[
                    ContentBlock(
                        type="text",
                        content=answer,
                    )
                ]
            ),
        )

        # STEP 5: EPISODIC + MEMORY EXTRACTION
        await self.episode_service.add_interaction(session_id=session_id, user_msg=msg, gideon_msg=answer)
        await self.episode_service.schedule_finalize(session_id)

        episode_id = None

        if self.memory_gate.should_extract(user_msg=msg, gideon_msg=answer):
            await self.memory_extractor.extract(
                user_msg=msg, 
                gideon_response=answer, 
                message_id=user_message_id, 
                episode_id=episode_id
            )

            await self.refresh_boot_cache()

        state = self.state_manager.get_state(session_id=session_id)
        updates = await self.state_extractor.extract(state=state, user_msg=msg, gideon_msg=answer)

        self.state_manager.update(session_id, **updates)


        # STEP 6: RETURN RESPONSE
        return answer