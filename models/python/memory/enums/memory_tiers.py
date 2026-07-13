from enum import Enum


class MemoryTier(str, Enum):
    
    WORKING = "working"
    EPISODIC = "episodic"       # types: episode, life_event
    SEMANTIC = "semantic"       # types: goal, project, fact
    IDENTITY = "identity"       # types: preference, value, belief
    PROCEDURAL = "procedural"   # types: workflow, skill, policy