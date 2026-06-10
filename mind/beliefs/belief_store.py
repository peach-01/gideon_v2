import json
from pathlib import Path

from mind.beliefs.belief_model import Belief


class BeliefStore:

    def __init__(self):
        self.path = Path(__file__).parent / "beliefs.json"

        if not self.path.exists():
            self.path.write_text("[]")


    def load(self) -> list[Belief]:
        data = json.loads(self.path.read_text())
        return [Belief(**item) for item in data]


    def save(self, beliefs: list[Belief]):
        self.path.write_text(json.dumps(
            [b.model_dump(mode="json") for b in beliefs],
            indent=2,
        ))