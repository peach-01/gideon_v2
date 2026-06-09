class MemoryCanonicalizer:

    def __init__(self, advisor_service):
        self.advisor = advisor_service

    async def canonicalize(self, content: str, memory_type: str):
        prompt = f"""
            Convert this memory into a canonical form.

            Rules:
            - Normalize wording.
            - Use third person.
            - Preserve meaning.
            - Output only ONE sentence.
            - Output only the canonical memory.

            
            Examples:

            Memory Type: preference
            Input: I love coffee
            Output: User likes coffee

            Memory Type: preference
            Input: Coffee is my favorite drink
            Output: User likes coffee

            Memory Type: preference
            Input: I drink coffee every day
            Output: User likes coffee

            Memory Type: goal
            Input: I want to build an AI OS
            Output: User wants to build an AI operating system

            Memory Type: project
            Input: I'm working on Gideon
            Output: User is working on the Gideon project

            
            Memory Type:
            {memory_type}

            Input:
            {content}
        """

        result = await self.advisor.ask(
            task="summarization",
            prompt=prompt,
        )

        return result.strip()