from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.dependencies import get_db
from database.models import Ticket, User
from schemas import TicketCreate, TicketResponse
from security import get_current_user

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