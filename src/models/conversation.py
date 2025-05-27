from typing import Optional

from pydantic import BaseModel


class Conversation(BaseModel):
    conversation_id: Optional[int] = None
    message: str
    user_id: Optional[str] = None
