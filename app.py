import asyncio
import uuid

from infrastructure.containers.container import Container
from runtime.orchestrator import Orchestrator


async def main():

    container = Container()

    await container.boot_manager.boot()

    orc = Orchestrator(container)

    await orc.wake()

    session_id = str(uuid.uuid4())


    while True:

        msg = input("\n> ")

        if msg == "/sleep":
            await orc.sleep()
            print("GIDEON sleeping.")
            continue

        if msg == "/wake":
            await orc.wake()
            print("GIDEON awake.")
            continue

        if msg == "/exit":
            await orc.sleep()
            break


        response = await orc.process(session_id=session_id, msg=msg)

        print(f"\nGIDEON: {response}\n")


asyncio.run(main())