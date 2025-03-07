from pydantic import BaseModel
from typing import Optional


class Conversation(BaseModel):
    conversation_id: Optional[int] =None
    message:str
