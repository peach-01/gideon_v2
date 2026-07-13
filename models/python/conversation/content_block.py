from dataclasses import dataclass, asdict


@dataclass
class ContentBlock:

    type: str
    content: str    # ex: text, voice recording, photo, sensor info, etc.

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)