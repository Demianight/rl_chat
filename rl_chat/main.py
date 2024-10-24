from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import apps
from rl_chat.exceptions import (
    DBInteractionException,
    JWTException,
    db_interaction_exception_handler,
    jwt_exception_handler,
)


app = FastAPI()

app.include_router(apps.core_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust based on your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(
    DBInteractionException,
    db_interaction_exception_handler,
)
app.add_exception_handler(
    JWTException,
    jwt_exception_handler,
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
