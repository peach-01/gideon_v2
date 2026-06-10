import json
from pathlib import Path

from mind.experiences.experience_model import Experience


class ExperienceStore:

    def __init__(self):
        self.path = Path(__file__).parent / "experiences.json"

        if not self.path.exists():
            self.path.write_text("[]")


    def load(self) -> list[Experience]:
        data = json.loads(self.path.read_text())
        return [
            Experience(**item)
            for item in data
        ]


    def save(self, experiences: list[Experience]):
        self.path.write_text(json.dumps(
            [
                e.model_dump(mode="json") 
                for e in experiences
            ],
            indent=2,
        ))