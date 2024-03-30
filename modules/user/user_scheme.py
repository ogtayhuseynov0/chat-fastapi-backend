from pydantic import BaseModel



class UserBase(BaseModel):
    username: str
    pass

class UserCreate(UserBase):
    password: str
    pass


class User(UserBase):
    id: int
    is_online: bool

    class Config:
        from_attributes = True
