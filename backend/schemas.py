from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TicketCreate(BaseModel):
    title: str
    description: str


class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    created_by: int
    assigned_to: int | None
    created_at: datetime

    model_config = {"from_attributes": True}