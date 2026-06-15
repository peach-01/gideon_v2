from enum import Enum


class MemoryType(str, Enum):

    # SEMANTIC
    FACT            = "fact"
    CONCEPT         = "concept"
    
    # USER MODEL
    PREFERENCE      = "preference"
    VALUE           = "value"
    BELIEF          = "belief"

    # PLANNING
    GOAL            = "goal"
    PROJECT         = "project"
    TASK            = "task"
    DECISION        = "decision"

    # SOCIAL
    PERSON          = "person"
    RELATIONSHIP    = "relationship"
    ORGANIZATION    = "organization"
    LOCATION        = "location"

    # EXPERIENCE
    EPISODE         = "episode"
    LIFE_EVENT      = "life_event"

    # SKILLS
    SKILL           = "skill"
    PROCEDURE       = "procedure"

    # SYSTEM
    WORKFLOW        = "workflow"    
    REFLECTION      = "reflection"
    POLICY          = "policy"