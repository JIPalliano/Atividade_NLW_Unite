import pytest
from .attendees_repository import AttendeesRepository
from src.models.settings.connection import db_connection_handler

db_connection_handler.connect_to_db()

@pytest.mark.skip(reason="Novo registro em banco de dados")
def test_insert_attendees():
    event_id = "123"
    attendeesinfo = {
        "uuid":"attendees123",
        "name": "atendees nome",
        "email": "email@email.com",
        "event_id": event_id
    }
    attendees_repository = AttendeesRepository()
    response = attendees_repository.insert_attendees(attendeesinfo)
    print(response)
  
@pytest.mark.skip(reason="Consulta no banco de dados")    
def test_get_attendees_by_id():
    attendee_id = "attendees123"
    attendees_repository = AttendeesRepository()
    attendee = attendees_repository.get_attendees_by_id(attendee_id)
    
    print(attendee)
    print(attendee.title)