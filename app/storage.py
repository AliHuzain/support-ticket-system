from typing import List, Optional
from uuid import uuid4
from datetime import datetime

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from .models import Ticket, TicketCreate, TicketStatus
from .db_models import TicketDB


def create_ticket(db: Session, payload: TicketCreate) -> Ticket:
    ticket_id = str(uuid4())
    now = datetime.utcnow()

    row = TicketDB(
        id=ticket_id,
        customer_name=payload.customer_name,
        title=payload.title,
        description=payload.description,
        priority=payload.priority.value,
        status=TicketStatus.open.value,
        created_at=now,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return _to_ticket(row)


def list_tickets(db: Session) -> List[Ticket]:
    rows = db.execute(select(TicketDB)).scalars().all()
    return [_to_ticket(r) for r in rows]


def get_ticket(db: Session, ticket_id: str) -> Optional[Ticket]:
    row = db.get(TicketDB, ticket_id)
    return _to_ticket(row) if row else None


def delete_ticket(db: Session, ticket_id: str) -> bool:
    result = db.execute(delete(TicketDB).where(TicketDB.id == ticket_id))
    db.commit()
    return result.rowcount > 0


def update_status(db: Session, ticket_id: str, new_status: TicketStatus) -> Optional[Ticket]:
    row = db.get(TicketDB, ticket_id)
    if not row:
        return None
    row.status = new_status.value
    db.commit()
    db.refresh(row)
    return _to_ticket(row)


def _to_ticket(row: TicketDB) -> Ticket:
    return Ticket(
        id=row.id,
        customer_name=row.customer_name,
        title=row.title,
        description=row.description,
        priority=row.priority,
        status=row.status,
        created_at=row.created_at,
    )