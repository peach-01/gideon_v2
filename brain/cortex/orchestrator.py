import json
import re

from runtime.services.llm_service import LLMService
from memory.memory_service import MemoryService
from memory.episodic_memory.conversations.converstation_service import ConversationService
from memory.semantic_memory.concepts.memory_extractor import MemoryExtractor
from consciousness.self_monitoring.state_extractor import StateExtractor
from consciousness.self_monitoring.state_manager_service import StateManager
from mind.self_model.identity_service import IdentityService

from brain.cortex.reasoning.context_builder import ContextBuilder

from nervous_system.signal_bus.schemas.tool_schemas import TOOL_SCHEMAS
from actions.tools.tool_application.tool_executor import ToolExecutor


MAX_TOOL_ROUNDS = 5


# ------------- HELPER --------------
def parse_json_response(text):
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    return json.loads(text.strip())


# -------------- CORE ----------------
class Orchestrator:

    def __init__(self):
        self.llm = LLMService()
        self.memory = MemoryService()
        self.conversation = ConversationService()
        self.tool_executor = ToolExecutor()
        self.state_manager = StateManager()
        self.identity = IdentityService()

        self.context_builder = ContextBuilder(self.memory, self.conversation, self.state_manager)
        self.memory_extractor = MemoryExtractor(self.llm, self.memory)
        self.state_extractor = StateExtractor(self.llm)


    async def process(self, session_id: str, msg: str):
        """FLOW: user msg -> store convo -> build context -> LLM call ->
            -> tool call? -> execute tool -> continue LLM ->
            -> store response -> extract memories -> return response
        """
        
        # STEP 1: STORE USER MSG
        await self.conversation.store_message(
            session_id=session_id,
            role="user",
            content=msg,
        )

        # STEP 2: BUILD CONTEXT
        context = await self.context_builder.build(session_id=session_id, query=msg)

        # STEP 3: BUILD INITIAL MESSAGES
        messages = [
            {
                "role": "system",
                "content": self.identity.system_prompt(),
            },
            {
                "role": "system",
                "content": context,
            },
            {
                "role": "user",
                "content": msg,
            }
        ]

        # STEP 3: LLM + TOOL LOOP
        tool_results = []

        for _ in range(MAX_TOOL_ROUNDS):
            response = await self.llm.chat(messages=messages, tools=TOOL_SCHEMAS)

            gideon_msg = {
                "role": "gideon",
                "content": response.content,
            }

            if response.tool_calls:
                gideon_msg["tool_calls"] = response.tool_calls

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
            role="gideon",
            content=answer,
        )

        # STEP 5: MEMORY EXTRACTION
        await self.memory_extractor.extract(user_msg=msg, gideon_response=answer)

        # STEP 6: UPDATE STATE
        state = self.state_manager.get_state(session_id=session_id)
        updates = await self.state_extractor.extract(state=state, user_msg=msg, gideon_msg=answer)

        self.state_manager.update(session_id, **updates)

        # STEP 6: RETURN RESPONSE
        return answer