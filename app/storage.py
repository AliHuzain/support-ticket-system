from typing import List, Optional
from uuid import uuid4
from datetime import datetime

from .models import Ticket, TicketCreate, TicketStatus


TICKETS: List[Ticket] = []


def create_ticket(payload: TicketCreate) -> Ticket:
    ticket = Ticket(
        id=str(uuid4()),
        customer_name=payload.customer_name,
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        status=TicketStatus.open,
        created_at=datetime.utcnow(),
    )
    TICKETS.append(ticket)
    return ticket


def list_tickets() -> List[Ticket]:
    return TICKETS


def get_ticket(ticket_id: str) -> Optional[Ticket]:
    for t in TICKETS:
        if t.id == ticket_id:
            return t
    return None


def delete_ticket(ticket_id: str) -> bool:
    for i, t in enumerate(TICKETS):
        if t.id == ticket_id:
            TICKETS.pop(i)
            return True
    return False


def update_status(ticket_id: str, new_status: TicketStatus) -> Optional[Ticket]:
    t = get_ticket(ticket_id)
    if not t:
        return None
    t.status = new_status
    return t