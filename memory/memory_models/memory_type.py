from enum import Enum


class MemoryType(str, Enum):

    FACT            = "fact"
    PREFERENCE      = "preference"
    GOAL            = "goal"
    PROJECT         = "project"

    PERSON          = "person"
    RELATIONSHIP    = "relationship"
    LOCATION        = "location"
    WORKFLOW        = "workflow"
    LIFE_EVENT      = "life_event"

    CONVERSATION    = "conversation"
    TASK            = "task"
    DECISION        = "decision"
    SKILL           = "skill"
    SYSTEM          = "system"