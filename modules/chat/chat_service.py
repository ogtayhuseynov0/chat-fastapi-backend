from operator import and_, or_
from sqlalchemy.orm import Session

from . import chat_scheme

import models


def read_chats(db: Session, user_id: int):
    return db.query(models.Chat).filter(or_(models.Chat.user1ID == user_id, models.Chat.user2ID == user_id)).all()


def create_chat(db: Session, chat: chat_scheme.ChatCreate):
    existed_chat = db.query(models.Chat) \
    .filter(or_(and_(models.Chat.user1ID == chat.user1ID, models.Chat.user2ID == chat.user2ID), and_(models.Chat.user2ID == chat.user1ID, models.Chat.user1ID == chat.user2ID))) \
    .first()
    if existed_chat:
        return existed_chat

    db_chat = models.Chat(**chat.model_dump())
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat


