import json
from pathlib import Path


class IdentityStore:

    def __init__(self):
        self.path = Path(__file__).parent / "identity.json"

    def load(self):
        with open(self.path, "r") as f:
            return json.load(f)

    def save(self, identity):
        with open(self.path, "w") as f:
            json.dump(identity, f, indent=2)