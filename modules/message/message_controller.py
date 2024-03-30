from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .message_service import insert_message, read_messages
from database import get_db
from . import message_scheme

message_router = APIRouter(
    prefix="/messages",
    tags=["Message"]
)


@message_router.get("/chat/{chat_id}", response_model=list[message_scheme.Message])
def get_chats(chat_id: int,  db: Session = Depends(get_db)):
    return read_messages(db, chat_id)

@message_router.post("/", response_model=message_scheme.Message)
def create_user(message: message_scheme.MessageCreate, db: Session = Depends(get_db)):
    return insert_message(db=db, message=message)


