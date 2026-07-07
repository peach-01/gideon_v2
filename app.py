import asyncio
import uuid

from runtime.orchestrator import Orchestrator


async def main():

    orc = Orchestrator()

    session_id = str(uuid.uuid4())

    while True:

        msg = input("\n> ")

        response = await orc.process(session_id=session_id, msg=msg)

        print(f"\nGIDEON: {response}\n")


asyncio.run(main())