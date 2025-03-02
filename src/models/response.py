from pydantic import BaseModel
from typing import Optional,List
from src.models.messsage import MessageResponse


class Response(BaseModel):
    conversation_id: int
    message:List[MessageResponse]
