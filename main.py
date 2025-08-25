from fastapi import FastAPI
import uuid
import datetime 
from app.models.user_input import UserInput
from app.models.kpm_ticket import KpmTicket  
from app.models.user_ticket import UserTicket  
from app.services.storage import  SQLiteStorage
from app.wk_orchestrator import WKOrchestrator

app = FastAPI()
storage = SQLiteStorage()
orchestrator = WKOrchestrator(storage)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post("/ticket")
async def create_ticket(user_input: UserInput) -> uuid.UUID:
    ticket_id = await orchestrator.add_ticket(user_input)
    return ticket_id

@app.get("/ticket/{ticket_id}")
def read_ticket(ticket_id: uuid.UUID):
    # Here you would typically fetch the ticket from a database
    ticket = orchestrator.get_kpm_ticket(ticket_id)
    if ticket:
        return ticket
    return {"error": "Ticket not found"}

@app.get("/ticket")
def read_tickets():
    # Here you would typically fetch the ticket from a database
    tickets = orchestrator.get_all_kpm_tickets()
    if tickets:
        return tickets
    return {"error": "No tickets found"}

@app.post("/chat")
async def chat(user_input: str):
    text = await orchestrator.chat(user_input)
    return text