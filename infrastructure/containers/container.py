from runtime.services.advisor_service import AdvisorService

from memory.memory_service import MemoryService

from memory.long_term_memory.episodic_memory.conversations.conversation_service import ConversationService
from memory.long_term_memory.semantic_memory.concepts.memory_extractor import MemoryExtractor
from memory.long_term_memory.episodic_memory.episode_service import EpisodeService
from memory.long_term_memory.semantic_memory.concepts.memory_gate import MemoryGate
from memory.long_term_memory.semantic_memory.embeddings.embedding_service import EmbeddingService
from memory.long_term_memory.semantic_memory.relations.entity_service import EntityService

from memory.storage.lineage.lineage_service import LineageService
from memory.storage.vector_memory.vector_memory_service import VectorMemoryService
from memory.storage.graph_memory.graph_service import GraphMemoryService

from evolution.self_reflection.reflection_service import ReflectionService

from brain.cortex.workspace.state_extractor import StateExtractor
from brain.cortex.workspace.state_manager_service import StateManager
from brain.cortex.cognition.cognitive_context_builder import ContextBuilder
from brain.frontal_lobe.goal_management.goal_manager import GoalManager

from mind.self_model.self_model_service import SelfModelService
from mind.self_model.self_model_formatter import SelfModelFormatter
from mind.identity.identity_service import IdentityService
from mind.beliefs.belief_service import BeliefService
from mind.experiences.experience_service import ExperienceService

from runtime.providers.openai_provider import OpenAIProvider
from runtime.providers.claude_provider import ClaudeProvider
from runtime.providers.gemini_provider import GeminiProvider
from runtime.providers.local_provider import LocalProvider

from genetics.initialization.cognitive_cache_service import CognitiveCacheService
from genetics.initialization.boot_manager import BootManager

from nervous_system.signal_bus.routers.advisor.intelligent_router import IntelligentRouter

from actions.tools.tool_application.tool_executor import ToolExecutor


class Container:

    def __init__(self):

        self.boot_manager = BootManager(self)

        # ----------- PROVIDERS ------------
        self.providers = {
            "gpt": OpenAIProvider(),
            "claude": ClaudeProvider(),
            "gemini": GeminiProvider(),
            "local": LocalProvider(),
        }

        # ----------- ROUTING ------------
        self.router = IntelligentRouter()

        # ----------- CORE ------------
        self.advisor_service = AdvisorService(
            intelligent_router=self.router,
            providers=self.providers
        )

        self.conversation_service = ConversationService()
        self.embedding_service = EmbeddingService()
        self.entity_service = EntityService()
        self.graph_memory_service = GraphMemoryService()
        self.identity_service = IdentityService()
        self.lineage_service = LineageService()
        self.memory_gate = MemoryGate()
        self.self_model_formatter = SelfModelFormatter()
        self.state_manager = StateManager()
        self.vector_service = VectorMemoryService()
        
        self.memory_service = MemoryService(advisor_service=self.advisor_service)
        self.goal_manager = GoalManager(memory_service=self.memory_service)
        self.state_extractor = StateExtractor(advisor_service=self.advisor_service)
        self.tool_executor = ToolExecutor(memory_service=self.memory_service)
        self.belief_service = BeliefService(memory_service=self.memory_service)
        self.experience_service = ExperienceService(memory_service=self.memory_service)
        self.reflection_service = ReflectionService(belief_service=self.belief_service)

        self.episode_service = EpisodeService(
            advisor=self.advisor_service, 
            memory_service=self.memory_service
        )

        self.memory_extractor = MemoryExtractor(
            advisor_service=self.advisor_service, 
            memory_service=self.memory_service, 
            graph_memory=self.graph_memory_service
        )

        self.self_model_service = SelfModelService(
            memory_service=self.memory_service, 
            identity_service=self.identity_service
        )

        self.cache_service = CognitiveCacheService(
            memory_service=self.memory_service,
            self_model_service=self.self_model_service,
            graph_service=self.graph_memory_service,
            formatter=self.self_model_formatter,
        )

        self.context_builder = ContextBuilder(
            memory_service=self.memory_service, 
            conversation_service=self.conversation_service, 
            state_manager=self.state_manager,
            identity_service=self.identity_service,
            cache=self.cache_service.cache,
            goal_manager=self.goal_manager
        )