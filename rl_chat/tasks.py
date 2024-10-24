import asyncio
from aiogram import Bot
from celery import Celery
from database import models
from rl_chat.settings import settings

app = Celery("tasks", broker="redis://localhost:6379/0")


def send_message(text: str, tg_id: int):
    """
    The simplest way to send message
    No other functionality is needed
    """
    
    bot = Bot(settings.bot.token)

    asyncio.run(
        bot.send_message(
            tg_id,
            text,
        ),
    )


@app.task
def notify_user(message_id: int, tg_id: int):
    message = get_message_helper(message_id)
    if not message:
        return

    text = f"Received new message: {message.content}\nAt {message.created_at}"

    send_message(text, tg_id)


def get_message_helper(message_id: int) -> models.Message | None:
    """
    db dependency makes this part a bit difficult
    Maybe better solution exists
    """
    db = models.SessionLocal()
    try:
        message = (
            db.query(models.Message)
            .filter(models.Message.id == message_id)
            .first()
        )

        return message

    finally:
        db.close()
