import asyncio

from datetime import datetime, UTC

from models.python.conversation.content_block import ContentBlock
from models.python.conversation.converstation_message import ConversationMessage
from models.python.awareness.processing_context import ProcessingContext
from models.python.working_state.runtime_state import RuntimeState

from nervous_system.signal_bus.schemas.tool_schemas import TOOL_SCHEMAS

from infrastructure.containers.container import Container



MAX_TOOL_ROUNDS = 5


# -------------- INITS ----------------
class Orchestrator:

    def __init__(self, container: Container):

        # runtime variables
        self.running = True
        self.background_tasks = []
        self.sessions = set()

        # core services
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

        if not self.running:
            raise RuntimeError("Orchestrator sleeping. Call wake() first.")
        self.sessions.add(session_id)
        
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

        task = asyncio.create_task(self._learn(ctx))
        self.background_tasks.append(task)
        
        return ctx.answer
    

    async def sleep(self):
        print("[ORC] Entering sleep mode")
        self.running = False

        await self._flush_learning()

        # stop accepting new work
        await self._pause_background_tasks()

        runtime_state = RuntimeState(
            status="sleeping",
            session_ids=list(self.sessions),

            pending_tasks=await self._collect_pending_tasks(),
            pending_reflections=await self._collect_reflections(),

            conversation_summary=await self._save_conversation_summary(),

            model_state=await self._save_model_state(),
            boot_cache=self.cache_service.cache,
        )

        await self.state_manager.save_runtime_state(runtime_state)
        await self.cache_service.refresh_boot()

        print("[ORC] Sleeping. State persisted.")



    async def wake(self):
        print("[ORC] Waking...")
        state = await self.state_manager.load_runtime_state()

        if not state:
            print("[ORC] No sleep state found.")
            self.running = True
            return

        self.sessions.update(state.session_ids)

        await self._restore_tasks(state.pending_tasks)
        await self._restore_reflections(state.pending_reflections)
        await self._restore_model_state(state.model_state)

        self.cache_service.cache = (state.boot_cache)

        self.running = True


        asyncio.create_task(self._resume_background_jobs())

        print("[ORC] Awake.")



    # -------- ASYNCED PROCESSING ---------
    async def _learn(self, ctx):
        try: 
            await self._extract_memories(ctx)
            await self.cache_service.refresh_boot()

        except Exception:
            print("[ERROR][ORC] Learning pipline failed")

        finally:
            current = asyncio.current_task()

            if current in self.background_tasks:
                self.background_tasks.remove(current)


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
        print("[LEARNING] extracting")

        await self.episode_service.add_interaction(
            session_id=ctx.session_id, 
            user_msg=ctx.user_message, 
            gideon_msg=ctx.answer
        )

        await self.episode_service.schedule_finalize(ctx.session_id)

        if self.memory_gate.should_extract(user_msg=ctx.user_message, gideon_msg=ctx.answer):
            print("[DEBUG][ORC] Memory extraction gate passed. Starting extract...")
            await self.cognition_extractor.extract(
                user_msg=ctx.user_message, 
                gideon_response=ctx.answer,

                message_id=ctx.user_message_id, 
                episode_id=ctx.episode_id,
                session_id=ctx.session_id,

                context=ctx,
            )



    # ------------- SLEEP HELPERS -------------
    async def _pause_background_tasks(self):
        for task in self.background_tasks:
            if not task.done():
                task.cancel()


    async def _collect_pending_tasks(self):
        if hasattr(self.tool_executor, "pending"):
            return self.tool_executor.pending
        return []


    async def _collect_reflections(self):
        if hasattr(self.episode_service, "pending_reflections"):
            return self.episode_service.pending_reflections
        return []


    async def _save_conversation_summary(self):
        return await self.conversation.summary()


    async def _save_model_state(self):
        return await self.self_model.export_state()
    

    async def _flush_learning(self):
        print("[ORC] Flushing learning pipeline...")

        for session_id in list(self.sessions):
            try:
                await self.episode_service.finalize_episode(session_id)

            except Exception as e:
                print(f"[ORC] Episode flush failed: {e}")


    # ------------ WAKE HELPERS -------------
    async def _restore_tasks(self, tasks):
        for task in tasks:
            await self.tool_executor.enqueue(task)


    async def _restore_reflections(self, reflections):
        for reflection in reflections:
            await self.episode_service.resume(reflection)


    async def _restore_model_state(self, state):
        await self.self_model.import_state(state)


    async def _resume_background_jobs(self):
        await self.cache_service.refresh_boot()
