# File: /C:/Users/rarod/Repos/rpr/agents/multiagents-web-api/app/wk_orchestrator.py
import uuid
import datetime 
from app.models.user_input import UserInput  
from app.models.kpm_ticket import KpmTicket
from app.services.storage import  SQLiteStorage
from app.services.wk_agent_service import AgentService

class WKOrchestrator:
    def __init__(self, storage_service: SQLiteStorage):
        """
        Initializes the orchestrator with a storage service.

        :param storage_service: An instance of the storage service to interact with.
        """
        self.storage_service = storage_service

    async def add_ticket(self, ticket_data: UserInput) -> uuid.UUID:
        """
        Adds a ticket to the storage.

        :param ticket_data: The data associated with the ticket.
        """
        ticket_id = uuid.uuid4()
        timestamp = datetime.datetime.now()
        kpm_ticket = KpmTicket(client_id=ticket_data.client_id, error_message=ticket_data.text, ticket_id=ticket_id, timestamp=timestamp, car_part="", error_description="", beanstandung="", link_to_logs="", severity="")
        await self._manage_ticket(kpm_ticket)
        return ticket_id

    def get_kpm_ticket(self, ticket_id):
        """
        Retrieves a ticket from the storage.

        :param ticket_id: The unique identifier for the ticket.
        :return: The data associated with the ticket, or None if not found.
        """

        return self.storage_service.get(ticket_id)
  
    def get_all_kpm_tickets(self):
        """
        Retrieves all tickets from the storage.
        :return: A list of all tickets, or an empty list if none found.
        """
        return self.storage_service.get_all()

    async def _manage_ticket(self, ticket: KpmTicket):      
        """
        Manages updates to an existing ticket by storing the updated ticket data asynchronously.
        :param ticket: An instance of KpmTicket containing the ticket's unique identifier 
                       and updated data to be stored.
        :return: None
        """
        self.storage_service.set(str(ticket.ticket_id), ticket)
    
    async def chat(self, text: str) -> str: 
        agent_service = AgentService()
        return await agent_service.chat_agent(text)