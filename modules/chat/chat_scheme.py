from pydantic import BaseModel

from ..user import user_scheme

class ChatBase(BaseModel):
    title: str | None = None
    pass

class ChatCreate(ChatBase):
    user1ID: int
    user2ID: int
    pass


class Chat(ChatCreate):
    id: int

    user1: user_scheme.User
    user2: user_scheme.User

    class Config:
        from_attributes = True
