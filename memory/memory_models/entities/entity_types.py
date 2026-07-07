from enum import Enum


class EntityType(str, Enum):

    PERSON          = "person"
    PROJECT         = "project"
    GOAL            = "goal"
    LOCATION        = "location"
    ORGANIZATION    = "organization"
    SKILL           = "skill"
    TOOL            = "tool"
    SYSTEM          = "system"
    TASK            = "task"
    CONCEPT         = "concept"
    EVENT           = "event"