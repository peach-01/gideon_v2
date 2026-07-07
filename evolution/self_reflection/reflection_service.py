from mind.beliefs.belief_service import BeliefService


class ReflectionService:

    def __init__(self):
        self.beliefs = BeliefService()


    def process_experience(self, experience):
        for lesson in experience.lessons:
            if self.beliefs.find(lesson):
                self.beliefs.reinforce(
                    statement=lesson, 
                    evidence=experience.title
                )

            else:
                self.beliefs.add(
                    statement=lesson,
                    domain="experience",
                    source="reflection",
                    confidence=experience.confidence,
                    evidence=[experience.title],
                )