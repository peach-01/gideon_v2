class BootManager:

    def __init__(self, container):
        self.container = container


    async def boot(self):

        print("[SYSTEM] Booting...")


        await self.boot_providers()

        await self.boot_storage()

        await self.boot_memory()

        await self.boot_current_state()

        await self.boot_capabilities()

        await self.build_cache()


        print("[SYSTEM] Boot complete.")



    async def boot_providers(self):
        pass


    async def boot_storage(self):

        await self.container.graph_memory_service.boot()

        await self.container.lineage_service.boot()

        await self.container.vector_service.boot()



    async def boot_memory(self):

        await self.container.advisor_service.boot()

        await self.container.belief_service.boot()

        await self.container.conversation_service.boot()

        await self.container.embedding_service.boot()

        await self.container.entity_service.boot()

        await self.container.episode_service.boot()

        await self.container.experience_service.boot()

        await self.container.goal_manager.boot()

        await self.container.memory_service.boot()

        await self.container.reflection_service.boot()


    
    async def boot_current_state(self):

        await self.container.identity_service.boot()

        await self.container.self_model_service.boot()

        await self.container.state_extractor.boot()

        await self.container.state_manager.boot()



    async def boot_capabilities(self):

        await self.container.tool_executor.boot()



    async def build_cache(self):

        await self.container.cache_service.refresh_cache()