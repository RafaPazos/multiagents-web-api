import uuid
import datetime 
from pydantic import BaseModel
from datetime import datetime

class KpmTicket(BaseModel):
    client_id: str
    ticket_id: uuid.UUID
    timestamp: datetime
    error_message: str
    beanstandung: str
    car_part: str
    error_description: str
    link_to_logs: str
    severity: str