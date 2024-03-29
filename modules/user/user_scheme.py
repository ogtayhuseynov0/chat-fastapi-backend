from pydantic import BaseModel

from ..chat import chat_scheme


class UserBase(BaseModel):
    username: str
    pass

class UserCreate(UserBase):
    password: str
    pass


class User(UserBase):
    id: int
    is_online: bool
    chats: list[chat_scheme.Chat]

    class Config:
        from_attributes = True
