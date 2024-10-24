from fastapi import APIRouter
from . import users, frontend, messages


core_router = APIRouter()

core_router.include_router(users.router)
core_router.include_router(frontend.router)
core_router.include_router(messages.router)
