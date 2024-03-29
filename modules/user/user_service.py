from sqlalchemy.orm import Session

from . import user_scheme

import models



def create_user(db: Session, user: user_scheme.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(username=user.username, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def read_online(db: Session):
    return db.query(models.User).filter(models.User.is_online == True).all()

