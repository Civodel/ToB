from pydantic import BaseModel


class MessageResponse(BaseModel):
    role:str
    messages :str