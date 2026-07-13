from google import genai
from genetics.base_configs.config import settings
from models.python.conversation.advisor_response import AdvisorResponse

client = genai.Client(api_key=settings.GEMINI_API_KEY)


class GeminiProvider:

    async def boot(self):
        print("[GEMINI] Ready.")


    async def generate(self, model, messages, system_prompt=""):
        response = await client.aio.models.generate_content(
            model=model,
            contents=messages["contents"],
            config={
                "system_instruction": system_prompt,
            },
        )

        return AdvisorResponse(
            content=response.text or "",
            provider="gemini",
            model=model,
        )