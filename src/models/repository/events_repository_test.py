# Ambiente de teste
import pytest
from src.models.settings.connection import db_connection_handler
from .events_repository import EventsRepository

db_connection_handler.connect_to_db()

#@pytest irá pular o test_insert_event para ir para o próximo
@pytest.mark.skip(reason="Novo registro em banco de dados")
def test_insert_event():
    event = {
        "uuid": "123",
        "title": "meu titulo",
        "details": "detalhes",
        "slug": "www.slug.com",
        "maximum_attendees": 20,
    }
    
    events_repository = EventsRepository()
    response = events_repository.insert_event(event)
    print(response)

def test_get_event_by_id():
    event_id = "123"
    events_repository = EventsRepository()
    response = events_repository.get_event_by_id(event_id)
    print(response)
    print(response.title)