from sqlalchemy.orm import Session

from . import message_scheme

import models


def read_messages(db: Session, chat_id: int):
    return db.query(models.Message).filter(models.Message.chat_id == chat_id).all()


def insert_message(db: Session, message: message_scheme.MessageCreate):
    db_message = models.Message(**message.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


