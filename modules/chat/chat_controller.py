from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .chat_service import read_chats, create_chat
from database import get_db
from . import chat_scheme

chat_router = APIRouter(
    prefix="/chats",
    tags=["Chats"]
)


@chat_router.get("/", response_model=list[chat_scheme.Chat])
def get_chats(user_id: int,  db: Session = Depends(get_db)):
    return read_chats(db, user_id)

@chat_router.post("/", response_model=chat_scheme.Chat)
def create_user(chat: chat_scheme.ChatCreate, db: Session = Depends(get_db)):
    return create_chat(db=db, chat=chat)


