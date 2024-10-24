import redis
from database.models import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_redis():
    r = redis.Redis(host="localhost", port=6379)
    try:
        yield r
    finally:
        r.close()
