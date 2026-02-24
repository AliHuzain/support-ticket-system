from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional

from .models import Ticket, TicketCreate, TicketStatus, TicketPriority, TicketStatusUpdate
from . import storage

app = FastAPI(title="Support Ticket System")


@app.get("/")
def health():
    return {"status": "ok", "service": "support-ticket-system"}


@app.post("/tickets", response_model=Ticket)
def create_ticket(payload: TicketCreate):
    return storage.create_ticket(payload)


@app.get("/tickets", response_model=List[Ticket])
def list_tickets(
    status: Optional[TicketStatus] = Query(default=None),
    priority: Optional[TicketPriority] = Query(default=None),
):
    tickets = storage.list_tickets()
    if status:
        tickets = [t for t in tickets if t.status == status]
    if priority:
        tickets = [t for t in tickets if t.priority == priority]
    return tickets


@app.get("/tickets/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: str):
    t = storage.get_ticket(ticket_id)
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return t


@app.patch("/tickets/{ticket_id}/status", response_model=Ticket)
def set_status(ticket_id: str, payload: TicketStatusUpdate):
    t = storage.update_status(ticket_id, payload.status)
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return t


@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: str):
    ok = storage.delete_ticket(ticket_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"message": "Ticket deleted", "id": ticket_id}