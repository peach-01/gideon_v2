class ReflectionService:

    def __init__(self, belief_service):
        self.beliefs = belief_service


    async def boot(self):
        print("[REFLECTION] Ready.")


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