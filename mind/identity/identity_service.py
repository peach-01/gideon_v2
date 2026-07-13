from mind.identity.identity_store import IdentityStore


class IdentityService:

    def __init__(self):
        self.store = IdentityStore()
        self.identity = self.store.load()

    
    async def boot(self):
        self._snapshot = self.snapshot()
        print("[IDENTITY] Ready.")


    def save(self):
        self.store.save(self.identity)

    def snapshot(self):
        return self.identity

    @property
    def name(self):
        return self.identity["identity"]["name"]

    @property
    def version(self):
        return self.identity["identity"]["version"]
    
    @property
    def purpose(self):
        return self.identity["purpose"]
    
    @property
    def mission(self):
        return self.identity["mission"]