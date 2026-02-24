from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional

from .models import Ticket, TicketCreate, TicketStatus, TicketPriority, TicketStatusUpdate
from . import storage

from fastapi import FastAPI, HTTPException, Query, Depends
from typing import List, Optional
from sqlalchemy.orm import Session

from .db import SessionLocal, engine
from .db_models import TicketDB
from .models import Ticket, TicketCreate, TicketStatus, TicketPriority, TicketStatusUpdate
from . import storage

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


@app.get("/tickets", response_model=List[Ticket])
def list_tickets(
    status: Optional[TicketStatus] = Query(default=None),
    priority: Optional[TicketPriority] = Query(default=None),
    db: Session = Depends(get_db),
):
    tickets = storage.list_tickets(db)
    if status:
        tickets = [t for t in tickets if t.status == status.value]
    if priority:
        tickets = [t for t in tickets if t.priority == priority.value]
    return tickets


@app.get("/tickets/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    t = storage.get_ticket(db, ticket_id)
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return t



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