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

from fastapi import HTTPException

@app.post("/tickets/{ticket_id}/close", response_model=Ticket)
def close_ticket(ticket_id: str):
    for t in TICKETS:
        if t.id == ticket_id:
            t.status = "Closed"
            return t
    raise HTTPException(status_code=404, detail="Ticket not found")


from fastapi import HTTPException

@app.get("/tickets/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: str):
    for t in TICKETS:
        if t.id == ticket_id:
            return t
    raise HTTPException(status_code=404, detail="Ticket not found")

@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: str):
    for i, t in enumerate(TICKETS):
        if t.id == ticket_id:
            TICKETS.pop(i)
            return {"message": "Ticket deleted", "id": ticket_id}
    raise HTTPException(status_code=404, detail="Ticket not found")