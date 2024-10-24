from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from apps.messages import crud
from apps.messages.schemas import Message
from apps.users.dependencies import (
    get_request_user,
    get_request_user_from_query_param_token,
)
from database.models import User
from rl_chat.dependencies import get_db
from rl_chat.tasks import get_message_helper, notify_user, send_message


router = APIRouter(prefix="/messages", tags=["messages"])

clients: dict[int, WebSocket] = {}


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    user: User = Depends(get_request_user_from_query_param_token),
    db: Session = Depends(get_db),
):
    await websocket.accept()
    clients[user.id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            message = Message.model_validate_json(data)

            updated_message = crud.create_message(db, message, user.id)
            message = Message(
                id=updated_message.id,
                content=updated_message.content,
                sender_id=updated_message.sender_id,
                receiver_id=updated_message.receiver_id,
                created_at=updated_message.created_at,
            )

            await clients[user.id].send_text(
                message.model_dump_json(),
            )
            if message.receiver_id in clients:
                crud.mark_message_as_seen(db, message.id)  # type: ignore
                await clients[message.receiver_id].send_text(
                    message.model_dump_json(),
                )
            elif updated_message.receiver.tg_id:
                notify_user.apply_async(
                    (updated_message.id, updated_message.receiver.tg_id),
                    countdown=5,
                )

    except WebSocketDisconnect:
        del clients[user.id]


@router.get("/with/{user_id}")
def get_messages_with_user(
    user_id: int,
    request_user: User = Depends(get_request_user),
    db: Session = Depends(get_db),
) -> list[Message]:
    crud.mark_messages_as_seen(db, request_user.id)
    return crud.get_messages_with_user(db, request_user.id, user_id)  # type: ignore


@router.get("/test")
def test():
    notify_user.apply_async(
        (40, 1650629059),
        countdown=5,
    )
