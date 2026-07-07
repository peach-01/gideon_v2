from pydantic import BaseModel


class Provenance(BaseModel):

    message_id: str | None = None
    episode_id: str | None = None

    origin_memory_id: str | None = None
    root_memory_id: str | None = None

    source_type: str | None = None