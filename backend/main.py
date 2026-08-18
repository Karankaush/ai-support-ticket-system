from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from database.dependencies import get_db

app = FastAPI(title="AI Support Ticket System")


@app.get("/")
def root():
    return {"message": "AI Support Ticket System API"}


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    return {"status": "ok"}