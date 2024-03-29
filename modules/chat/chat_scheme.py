from pydantic import BaseModel


class ChatBase(BaseModel):
    pass

class ChatCreate(ChatBase):
    owner_id: int
    second_user: int
    pass


class Chat(ChatBase):
    id: int

    class Config:
        from_attributes = True
