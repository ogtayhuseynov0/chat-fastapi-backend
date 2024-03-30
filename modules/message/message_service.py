from sqlalchemy.orm import Session

from . import message_scheme
from ..ws import ws_controller
import models


def read_messages(db: Session, chat_id: int):
    return db.query(models.Message).filter(models.Message.chat_id == chat_id).all()


async def insert_message(db: Session, message: message_scheme.MessageCreate):
    db_message = models.Message(**message.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    if db_message:
        await ws_controller.manager.send_message_clinet(message.chat_id, db_message, db)
    return db_message


