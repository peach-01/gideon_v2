class ClaudeProvider:

    async def boot(self):
        print("[CLAUDE] Ready.")


    async def generate(self, model, messages, system_prompt=""):
        raise NotImplementedError()