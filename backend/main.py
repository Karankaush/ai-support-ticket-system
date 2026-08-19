from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from database.models import User
from security import get_current_user
from database.dependencies import get_db
from routers.auth import router as auth_router
from routers.tickets import router as tickets_router
from redis_client import redis_client

app = FastAPI(title="AI Support Ticket System")

app.include_router(auth_router)
app.include_router(tickets_router)


@app.get("/redis-health")
def redis_health():
    redis_client.set("health_check", "ok")

    value = redis_client.get("health_check")

    return {
        "redis": value
    }


@app.get("/")
def root():
    return {"message": "AI Support Ticket System API"}


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    return {"status": "ok"}


@app.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
    }