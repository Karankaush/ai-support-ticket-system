from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.dependencies import get_db
from database.models import Ticket, User
from schemas import TicketCreate, TicketResponse
from security import get_current_user
from fastapi import HTTPException




router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post(
    "",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ticket(
    ticket_data: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = Ticket(
        title=ticket_data.title,
        description=ticket_data.description,
        created_by=current_user.id,
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket



@router.get("", response_model=list[TicketResponse])
def get_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(Ticket)

    if current_user.role == "CUSTOMER":
        query = query.where(Ticket.created_by == current_user.id)

    return db.scalars(query).all()




@router.patch("/{ticket_id}/assign", response_model=TicketResponse)
def assign_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "AGENT":
        raise HTTPException(
            status_code=403,
            detail="Only agents can assign tickets",
        )

    ticket = db.get(Ticket, ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    if ticket.assigned_to is not None:
        raise HTTPException(
            status_code=409,
            detail="Ticket is already assigned",
        )

    ticket.assigned_to = current_user.id

    db.commit()
    db.refresh(ticket)

    return ticket



@router.patch("/{ticket_id}/status", response_model=TicketResponse)
def update_ticket_status(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "AGENT":
        raise HTTPException(
            status_code=403,
            detail="Only agents can update ticket status",
        )

    ticket = db.get(Ticket, ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    if ticket.assigned_to != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only update your assigned tickets",
        )

    if data.status not in {"OPEN", "IN_PROGRESS", "RESOLVED"}:
        raise HTTPException(
            status_code=400,
            detail="Invalid ticket status",
        )

    ticket.status = data.status

    db.commit()
    db.refresh(ticket)

    return ticket

