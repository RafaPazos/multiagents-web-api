from pydantic import BaseModel
from datetime import datetime

class UserInput(BaseModel):
    text: str
    client_id: str