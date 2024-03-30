from dataclasses import dataclass
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    hashed_password = Column(String)
    is_online = Column(Boolean, default=False)

    chats = relationship("Chat", back_populates="owner")
    messages = relationship("Message", back_populates="owner")


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    second_user = Column(String)

    owner = relationship("User", back_populates="chats")
    messages = relationship("Message", back_populates="chat")

@dataclass
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    content = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    chat_id = Column(Integer, ForeignKey("chats.id"))
    created_at = Column(DateTime, default=func.now())
    owner = relationship("User", back_populates="messages")
    chat = relationship("Chat", back_populates="messages")

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

