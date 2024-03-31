from datetime import datetime
from pydantic import BaseModel
from ..user import user_scheme

class MessageBase(BaseModel):
    chat_id: int
    sender_id: int
    receiver_id: int
    content: str
    pass

class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: int
    created_at: datetime
    sender: user_scheme.User
    receiver: user_scheme.User

    class Config:
        from_attributes = True
