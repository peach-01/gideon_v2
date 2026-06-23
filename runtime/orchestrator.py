from runtime.services.advisor_service import AdvisorService

from memory.memory_service import MemoryService
from memory.long_term_memory.episodic_memory.conversations.conversation_service import ConversationService
from memory.long_term_memory.semantic_memory.concepts.memory_extractor import MemoryExtractor
from memory.long_term_memory.episodic_memory.episode_service import EpisodeService
from memory.storage.graph_memory.graph_service import GraphMemoryService
from memory.long_term_memory.episodic_memory.conversations.conversation_models.content_block import ContentBlock
from memory.long_term_memory.episodic_memory.conversations.conversation_models.converstation_message import ConversationMessage

from brain.cortex.workspace.state_extractor import StateExtractor
from brain.cortex.workspace.state_manager_service import StateManager
from brain.cortex.workspace.context_builder import ContextBuilder

from mind.self_model.self_model_service import SelfModelService
from mind.self_model.self_model_formatter import SelfModelFormatter
from mind.identity.identity_service import IdentityService

from nervous_system.signal_bus.schemas.tool_schemas import TOOL_SCHEMAS

from actions.tools.tool_application.tool_executor import ToolExecutor


MAX_TOOL_ROUNDS = 5


# -------------- CORE ----------------
class Orchestrator:

    def __init__(self):
        self.advisor = AdvisorService()

        self.memory = MemoryService(advisor_service=self.advisor)
        self.conversation = ConversationService()
        self.tool_executor = ToolExecutor(self.memory)
        self.state_manager = StateManager()
        self.graph_memory = GraphMemoryService()
        self.identity = IdentityService()

        self.self_model = SelfModelService(memory_service=self.memory, identity_service=self.identity)
        self.self_model_formatter = SelfModelFormatter()

        self.episode_service = EpisodeService(advisor=self.advisor, memory_service=self.memory)

        self.context_builder = ContextBuilder(
            memory_service=self.memory, 
            conversation_service=self.conversation, 
            state_manager=self.state_manager,
            identity_service=self.identity,
        )
        self.memory_extractor = MemoryExtractor(advisor_service=self.advisor, memory_service=self.memory, graph_memory=self.graph_memory)
        self.state_extractor = StateExtractor(advisor_service=self.advisor)


    async def process(self, session_id: str, msg: str):
        """FLOW: user msg -> store convo -> build context -> LLM call ->
            -> tool call? -> execute tool -> continue LLM ->
            -> store response -> extract memories -> return response
        """
        
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
        context = await self.context_builder.build(session_id=session_id, query=msg)
        snapshot = await self.self_model.snapshot()
        formatted_snap = self.self_model_formatter.format(snapshot=snapshot)

        # STEP 3: BUILD INITIAL MESSAGES
        messages = [
            ConversationMessage(
                role="system",
                content=[
                    ContentBlock(
                        type="text",
                        content=formatted_snap,
                    ),
                    ContentBlock(
                        type="text",
                        content=context,
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
            response = await self.advisor.ask(
                task="reasoning", 
                messages=messages,
            )

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

        # STEP 5: EPISODIC MEMORY EXTRACTION
        episode = await self.episode_service.create_episode(session_id=session_id, messages=messages)

        await self.memory_extractor.extract(
            user_msg=msg, 
            gideon_response=answer, 
            message_id=user_message_id, 
            episode_id=episode.id
        )

        # STEP 6: UPDATE STATE
        state = self.state_manager.get_state(session_id=session_id)
        updates = await self.state_extractor.extract(state=state, user_msg=msg, gideon_msg=answer)

        self.state_manager.update(session_id, **updates)

        # STEP 6: RETURN RESPONSE
        return answer