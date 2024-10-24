from fastapi import HTTPException, Request


class RLChatException(Exception):
    pass


class DBInteractionException(RLChatException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class JWTException(RLChatException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


def db_interaction_exception_handler(
    request: Request, exc: DBInteractionException
):
    raise HTTPException(
        status_code=400,
        detail=exc.message,
    )


def jwt_exception_handler(request: Request, exc: JWTException):
    raise HTTPException(
        status_code=401,
        detail=exc.message,
    )
