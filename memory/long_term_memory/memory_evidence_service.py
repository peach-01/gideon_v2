class MemoryEvidenceService:

    async def boot(self):
        print("[MEMORY-EVIDENCE] Ready.")

    async def add_evidence(self, memory_id: str, message_id: str, episode_id: str, confidence: float=1.0):
        return NotImplementedError
    
    def reinforce(self):
        return NotImplementedError