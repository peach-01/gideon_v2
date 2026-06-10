from mind.identity.identity_service import IdentityService
from mind.beliefs.belief_service import BeliefService
from mind.experiences.experience_service import ExperienceService

from mind.self_model.self_model import SelfModel


class SelfModelService:

    def __init__(self):
        self.identity = IdentityService()
        self.beliefs = BeliefService()
        self.experiences = ExperienceService()


    def snapshot(self):
        return SelfModel(
            identity=self.identity.identity,
            beliefs=self.beliefs.all(),
            experiences=self.experiences.all(),
        )