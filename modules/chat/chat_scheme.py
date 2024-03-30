from pydantic import BaseModel

from ..user import user_scheme

class ChatBase(BaseModel):
    pass

class ChatCreate(ChatBase):
    owner_id: int
    second_user: str
    pass


class Chat(ChatBase):
    id: int

    class Config:
        from_attributes = True
