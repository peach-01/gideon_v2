class AgentBus:

    def __init__(self):
        self.data = {}


    def publish(self, key, val):
        self.data[key] = val

    
    def get(self, key, default=None):
        return self.data.get(key, default)