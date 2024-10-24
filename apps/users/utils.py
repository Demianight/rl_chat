from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
from rl_chat.exceptions import JWTException
from rl_chat.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_jwt_token(
    data: dict,
) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(days=30)})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.token.secret_key,
        algorithm=settings.token.algorithm,
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    try:
        decoded_jwt = jwt.decode(
            token,
            settings.token.secret_key,
            algorithms=[settings.token.algorithm],
        )
        return decoded_jwt
    except jwt.ExpiredSignatureError:
        raise JWTException("Token has expired")
    except jwt.InvalidTokenError:
        raise JWTException("Decoded invalid token")
