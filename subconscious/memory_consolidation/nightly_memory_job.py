from subconscious.memory_consolidation.memory_consolidator import MemoryConsolidator

async def run():
    consolidator = MemoryConsolidator()

    await consolidator.consolidate()