from fastapi import FastAPI

from brain.cortex.orchestrator import Orchestrator
from interfaces.api.chat_request import ChatRequest

app = FastAPI()

gideon = Orchestrator()


@app.post("/chat")
async def chat(payload: ChatRequest):
    response = await gideon.process(session_id=payload.session_id, msg=payload.message)
    return {"response": response}