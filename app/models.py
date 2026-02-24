from __future__ import annotations
from enum import Enum
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class TicketStatus(str, Enum):
    open = "Open"
    in_progress = "In Progress"
    closed = "Closed"


class TicketPriority(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"


class TicketCreate(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=50)
    title: str = Field(..., min_length=3, max_length=80)
    description: str = Field(..., min_length=3, max_length=500)
    priority: TicketPriority = TicketPriority.medium


class Ticket(BaseModel):
    id: str
    customer_name: str
    title: str
    description: str
    priority: TicketPriority
    status: TicketStatus
    created_at: datetime


class TicketStatusUpdate(BaseModel):
    status: TicketStatus


class TicketListResponse(BaseModel):
    total: int
    items: List[Ticket]
    limit: int
    offset: int