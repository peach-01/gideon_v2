from enum import Enum


class MemoryType(str, Enum):

    FACT            = "fact"
    PREFERENCE      = "preference"
    GOAL            = "goal"
    PROJECT         = "project"
    PERSON          = "person"
    CONVERSATION    = "conversation"
    TASK            = "task"
    DECISION        = "decision"
    SKILL           = "skill"
    SYSTEM          = "system"