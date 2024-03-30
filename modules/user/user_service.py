from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import user_scheme

import models



def create_user(db: Session, user: user_scheme.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    is_in_db = db.query(models.User).filter(models.User.username == user.username).first()
    if is_in_db:
        if is_in_db.hashed_password == fake_hashed_password: # type: ignore
            return is_in_db
        else:
            raise HTTPException(status_code=403, detail="Credentials do not match.")

    db_user = models.User(username=user.username, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def read_online(db: Session):
    return db.query(models.User).filter(models.User.is_online == True).all()

def set_online(db: Session, user_name: str, is_online: bool = True):
    db_user = db.query(models.User).filter(models.User.username == user_name).first()
    
    if db_user is None:
        return None
    db_user.is_online = is_online # type: ignore
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


