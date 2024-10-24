from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from database.models import User
from rl_chat.exceptions import DBInteractionException

from . import utils, crud
from rl_chat.dependencies import get_db
from sqlalchemy.orm import Session


BearerToken = HTTPBearer()


def get_request_user(
    raw_token: HTTPAuthorizationCredentials = Depends(BearerToken),
    db: Session = Depends(get_db),
) -> User:
    data = utils.decode_access_token(raw_token.credentials)

    if user := crud.get_user_by_username(db, data["username"]):
        return user

    raise DBInteractionException("Invalid username")


def get_request_user_from_query_param_token(
    token: str,
    db: Session = Depends(get_db),
) -> User:
    if user := crud.get_user_by_username(
        db, utils.decode_access_token(token)["username"]
    ):
        return user

    raise DBInteractionException("Invalid username")
