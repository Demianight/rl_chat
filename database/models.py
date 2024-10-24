from datetime import datetime
from sqlalchemy import ForeignKey, Integer, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
    sessionmaker,
)

from rl_chat.settings import settings


class Base(DeclarativeBase):
    pass


class Model(Base):
    __abstract__ = True

    @declared_attr
    def id(cls) -> Mapped[int]:
        return mapped_column(Integer, primary_key=True, index=True)


class User(Model):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    tg_id: Mapped[int] = mapped_column(nullable=True, unique=True)

    sent_messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="sender",
        foreign_keys="Message.sender_id",
    )

    received_messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="receiver",
        foreign_keys="Message.receiver_id",
    )


class Message(Model):
    __tablename__ = "messages"

    content: Mapped[str] = mapped_column(nullable=False)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    receiver_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now
    )

    seen: Mapped[bool] = mapped_column(nullable=False, default=False)

    sender: Mapped["User"] = relationship(
        "User",
        back_populates="sent_messages",
        foreign_keys=[sender_id],
    )
    receiver: Mapped["User"] = relationship(
        "User",
        back_populates="received_messages",
        foreign_keys=[receiver_id],
    )


engine = create_engine(settings.postgres.url)
SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)
