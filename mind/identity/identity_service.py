from mind.identity.identity_store import IdentityStore


class IdentityService:

    def __init__(self):
        self.store = IdentityStore()
        self.identity = self.store.load()

    def save(self):
        self.store.save(self.identity)

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
    
    def get_peronality(self):
        return self.identity.get("personality", {})

    def get_values(self):
        return self.identity.get("values", {})

    def get_behavioral_policies(self):
        return self.identity.get("behavioral_policies", {})

    def get_advisor_preferences(self):
        return self.identity.get("advisor_preferences", {})

    def get_operating_modes(self):
        return self.identity.get("operating_modes", {})
    

    def update_value(self, path: list[str], value):
        node = self.identity

        for key in path[:-1]:
            node = node[key]

        node[path[-1]] = value

        self.save()

    def snapshot(self):
        return self.identity