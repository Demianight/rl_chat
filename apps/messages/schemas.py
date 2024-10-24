from datetime import datetime
from pydantic import BaseModel


class Message(BaseModel):
    id: int | None = None
    content: str
    sender_id: int | None = None
    receiver_id: int
    created_at: datetime | None = None
