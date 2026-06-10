from pydantic import BaseModel

from mind.beliefs.belief_model import Belief
from mind.experiences.experience_model import Experience


class SelfModel(BaseModel):

    identity: dict

    beliefs: list[Belief] = []

    experiences: list[Experience] = []