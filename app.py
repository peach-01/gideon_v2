import asyncio
import uuid

from infrastructure.containers.container import Container
from runtime.orchestrator import Orchestrator


async def main():

    container = Container()

    await container.boot_manager.boot()

    orc = Orchestrator(container)

    session_id = str(uuid.uuid4())


    while True:

        msg = input("\n> ")

        response = await orc.process(session_id=session_id, msg=msg)

        print(f"\nGIDEON: {response}\n")


asyncio.run(main())