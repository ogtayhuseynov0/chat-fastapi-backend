from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .user_service import create_user, read_online
from database import get_db
from . import user_scheme

user_router = APIRouter(
    prefix="/user",
    tags=["Auth"]
)

@user_router.post("/register", response_model=user_scheme.User)
def register(user: user_scheme.UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)

@user_router.get("/online", response_model=list[user_scheme.User])
def get_actives(db: Session = Depends(get_db)):
    return read_online(db=db)



