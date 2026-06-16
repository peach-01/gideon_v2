import asyncio

from runtime.orchestrator import Orchestrator


async def main():

    orc = Orchestrator()

    while True:

        msg = input("> ")

        response = await orc.process(session_id="test_session", msg=msg)

        print("\nGIDEON: ")
        print(response)
        print()


asyncio.run(main())