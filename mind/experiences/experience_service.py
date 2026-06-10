from mind.experiences.experience_model import Experience
from mind.experiences.experience_store import ExperienceStore


class ExperienceService:

    def __init__(self):
        self.store = ExperienceStore()
        self.experiences = self.store.load()


    def all(self):
        return self.experiences
    

    def add(self, title: str, summary: str, outcome: str, lessons: list[str], confidence: float=0.5):
        experience = Experience(title=title, summary=summary, outcome=outcome, lessons=lessons, confidence=confidence)

        self.experiences.append(experience)
        self.store.save(self.experiences)

        return experience