from sqlalchemy.orm import Session
from database import models
from rl_chat.exceptions import DBInteractionException
from . import schemas, utils


def create_user(db: Session, obj_in: schemas.UserCreate) -> models.User:
    if get_user_by_username(db, obj_in.username):
        raise DBInteractionException("Username already exists")

    db_obj = models.User(
        username=obj_in.username,
        password=utils.hash_password(obj_in.password),
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_user(db: Session, id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == id).first()


def get_user_by_username(db: Session, username: str) -> models.User | None:
    return (
        db.query(models.User).filter(models.User.username == username).first()
    )


def get_users(
    db: Session, skip: int = 0, limit: int = 100
) -> list[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def get_chat_users(db: Session, exclude_id: int) -> list[models.User]:
    return (
        db.query(models.User)
        .filter(models.User.id != exclude_id)
        .order_by(models.User.username)
        .all()
    )


def update_user(
    db: Session, user: models.User, obj_in: schemas.UserUpdate
) -> models.User:
    if obj_in.username:
        user.username = obj_in.username
    if obj_in.password:
        user.password = utils.hash_password(obj_in.password)
    if obj_in.tg_id:
        user.tg_id = obj_in.tg_id
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
