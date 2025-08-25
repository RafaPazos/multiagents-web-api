import uuid
from pydantic import BaseModel
from datetime import datetime

class UserTicket(BaseModel):
    client_id: str
    ticket_id: uuid.UUID
    timestamp: datetime
    error_message: str