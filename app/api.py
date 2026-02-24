from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from uuid import uuid4

app = FastAPI(title="Support Ticket System")

class TicketCreate(BaseModel):
    title: str
    description: str

class Ticket(BaseModel):
    id: str
    title: str
    description: str
    status: str

TICKETS: List[Ticket] = []

@app.get("/")
def health():
    return {"status": "ok", "service": "support-ticket-system"}

@app.post("/tickets", response_model=Ticket)
def create_ticket(payload: TicketCreate):
    ticket = Ticket(
        id=str(uuid4()),
        title=payload.title,
        description=payload.description,
        status="Open",
    )
    TICKETS.append(ticket)
    return ticket

@app.get("/tickets", response_model=List[Ticket])
def list_tickets():
    return TICKETS

@app.post("/tickets/{ticket_id}/close", response_model=Ticket)
def close_ticket(ticket_id: str):
    for t in TICKETS:
        if t.id == ticket_id:
            t.status = "Closed"
            return t
    return {"error": "Ticket not found"}