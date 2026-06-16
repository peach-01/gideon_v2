from memory.memory_models.basic_memory.memory_tiers import MemoryTier
from memory.memory_models.basic_memory.memory_type import MemoryType


TYPE_TO_TIER = {

    MemoryType.FACT: MemoryTier.SEMANTIC,
    MemoryType.CONCEPT: MemoryTier.SEMANTIC,
    MemoryType.GOAL: MemoryTier.SEMANTIC,
    MemoryType.PROJECT: MemoryTier.SEMANTIC,
    MemoryType.TASK: MemoryTier.SEMANTIC,
    MemoryType.DECISION: MemoryTier.SEMANTIC,

    MemoryType.BELIEF: MemoryTier.IDENTITY,
    MemoryType.PREFERENCE: MemoryTier.IDENTITY,
    MemoryType.VALUE: MemoryTier.IDENTITY,

    MemoryType.EPISODE: MemoryTier.EPISODIC,
    MemoryType.LIFE_EVENT: MemoryTier.EPISODIC,

    MemoryType.SKILL: MemoryTier.PROCEDURAL,
    MemoryType.PROCEDURE: MemoryTier.PROCEDURAL,
    MemoryType.WORKFLOW: MemoryTier.PROCEDURAL,
    MemoryType.POLICY: MemoryTier.PROCEDURAL,
}


def get_tier(memory_type):
    return TYPE_TO_TIER.get(memory_type, MemoryTier.SEMANTIC)