from fastapi import FastAPI

app = FastAPI(title="AI Support Ticket System")


@app.get("/")
def root():
    return {"message": "AI Support Ticket System API"}