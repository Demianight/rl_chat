from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from apps.users.dependencies import get_request_user
from database.models import User
from rl_chat.dependencies import get_db
from rl_chat.exceptions import DBInteractionException
from . import crud, schemas, utils


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def retrieve_users(db: Session = Depends(get_db)) -> list[schemas.User]:
    return crud.get_users(db)  # type: ignore


@router.get("/chat_users")
def retrieve_chat_users(
    db: Session = Depends(get_db), user: User = Depends(get_request_user)
) -> list[schemas.User]:
    return crud.get_chat_users(db, user.id)  # type: ignore


@router.post("/", status_code=201)
def create_user(
    obj_in: schemas.UserCreate, db: Session = Depends(get_db)
) -> schemas.User:
    return crud.create_user(db, obj_in)  # type: ignore


@router.post("/login")
def login(
    obj_in: schemas.UserCreate, db: Session = Depends(get_db)
) -> dict[str, str]:
    if not (obj := crud.get_user_by_username(db, obj_in.username)):
        raise DBInteractionException("Invalid username")
    if not utils.verify_password(obj_in.password, obj.password):
        raise DBInteractionException("Invalid password")

    token = utils.create_jwt_token({"username": obj_in.username})
    return {"token": token}


@router.get("/me")
def get_me(user: User = Depends(get_request_user)) -> schemas.User:
    return user  # type: ignore


@router.patch("/me")
def update_me(
    obj_in: schemas.UserUpdate,
    user: User = Depends(get_request_user),
    db: Session = Depends(get_db),
) -> schemas.User:
    return crud.update_user(db, user, obj_in)  # type: ignore
