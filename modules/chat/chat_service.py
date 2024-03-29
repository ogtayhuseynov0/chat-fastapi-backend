from sqlalchemy.orm import Session

from . import chat_scheme

import models


def read_chats(db: Session, user_id: int):
    return db.query(models.Chat).filter(models.Chat.owner_id == user_id).all()


def create_chat(db: Session, chat: chat_scheme.ChatCreate):
    db_chat = models.Chat(**chat.model_dump())
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat


