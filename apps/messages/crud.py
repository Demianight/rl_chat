from sqlalchemy.orm import Query, Session
from database import models
from . import schemas


def create_message(
    db: Session, obj_in: schemas.Message, sender_id: int
) -> models.Message:
    db_obj = models.Message(
        content=obj_in.content,
        sender_id=sender_id,
        receiver_id=obj_in.receiver_id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_messages(db: Session) -> list[models.Message]:
    return db.query(models.Message).all()


def get_messages_with_user(
    db: Session, sender_id: int, receiver_id: int
) -> list[models.Message]:
    return (
        db.query(models.Message)
        .filter(
            (
                (models.Message.sender_id == sender_id)
                & (models.Message.receiver_id == receiver_id)
            )
            | (
                (models.Message.sender_id == receiver_id)
                & (models.Message.receiver_id == sender_id)
            )
        )
        .all()
    )


def mark_messages_as_seen(db: Session, user_id: int):
    db.query(models.Message).filter(
        (models.Message.receiver_id == user_id)
        & (models.Message.seen.is_(False)),
    ).update({"seen": True})
    db.commit()


def mark_message_as_seen(db: Session, message_id: int):
    db.query(models.Message).filter(models.Message.id == message_id).update(
        {"seen": True}
    )
    db.commit()


def get_message_by_id(db: Session, message_id: int) -> models.Message | None:
    return (
        db.query(models.Message)
        .filter(models.Message.id == message_id)
        .first()
    )
