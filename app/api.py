from fastapi import FastAPI, HTTPException, Query, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from .db import SessionLocal, engine
from .db_models import TicketDB
from .models import Ticket, TicketCreate, TicketStatus, TicketPriority, TicketStatusUpdate
from . import storage
from .models import TicketListResponse

TicketDB.metadata.create_all(bind=engine)
app = FastAPI(title="Support Ticket System")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def health():
    return {"status": "ok", "service": "support-ticket-system"}


@app.post("/tickets", response_model=Ticket)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db)):
    return storage.create_ticket(db, payload)


@app.get("/tickets", response_model=TicketListResponse)
def list_tickets(
    status: Optional[TicketStatus] = Query(default=None),
    priority: Optional[TicketPriority] = Query(default=None),
    q: Optional[str] = Query(default=None, description="Search in title/description"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    total = storage.count_tickets(
        db=db,
        status=status.value if status else None,
        priority=priority.value if priority else None,
        q=q,
    )
    items = storage.list_tickets(
        db=db,
        status=status.value if status else None,
        priority=priority.value if priority else None,
        q=q,
        limit=limit,
        offset=offset,
    )
    return {"total": total, "items": items, "limit": limit, "offset": offset}


@app.get("/tickets", response_model=List[Ticket])
def list_tickets(
    status: Optional[TicketStatus] = Query(default=None),
    priority: Optional[TicketPriority] = Query(default=None),
    q: Optional[str] = Query(default=None, description="Search in title/description"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    return storage.list_tickets(
        db=db,
        status=status.value if status else None,
        priority=priority.value if priority else None,
        q=q,
        limit=limit,
        offset=offset,
    )



@app.patch("/tickets/{ticket_id}/status", response_model=Ticket)
def set_status(ticket_id: str, payload: TicketStatusUpdate, db: Session = Depends(get_db)):
    t = storage.update_status(db, ticket_id, payload.status)
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return t


@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: str, db: Session = Depends(get_db)):
    ok = storage.delete_ticket(db, ticket_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"message": "Ticket deleted", "id": ticket_id}