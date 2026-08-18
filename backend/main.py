from fastapi import FastAPI

from database.connection import engine

app = FastAPI(title="AI Support Ticket System")


@app.get("/")
def root():
    with engine.connect():
        return {"message": "Database connected"}