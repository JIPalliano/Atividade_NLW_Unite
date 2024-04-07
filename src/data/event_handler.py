import uuid
from src.http_types.http_request import HttpRequest
from src.http_types.http_response import HttpResponse
from src.errors.error_types.http_not_found import HttpNotFoundError
from src.models.repository.events_repository import EventsRepository

class EventHandler:
    def __init__(self) -> None:
        self.__events_repository = EventsRepository()
        
    def register(self, http_request: HttpRequest) -> HttpResponse:
        body = http_request.body
        body["uuid"] = str(uuid.uuid4())
        self.__events_repository.insert_event(body)
        
        return HttpResponse(
            body={"eventId": body["uuid"]},
            status_code=200
        )
        
    def find_by_id(self, http_request:HttpRequest) -> HttpResponse:
        event_id = http_request.param["event_id"]
        event = self.__events_repository.get_event_by_id(event_id)
        if not event: raise HttpNotFoundError("Evento não encontrado")
        
        event_attendees_count = self.__events_repository.count_event_attendees(event_id)
        
        return HttpResponse(
            body={
                "event":{
                    "id": event.id,
                    "title": event.title,
                    "details": event.details,
                    "slug": event.slug,
                    "maximumAttendees": event.maximum_attendees,
                    "attendeesAmount": event_attendees_count["attendeesAmount"]
                }
            },
            status_code=200
        )
        
    def exclude_event(self, http_request: HttpRequest) -> HttpResponse:
        event_id = http_request.param["event_id"]
        self.__events_repository.exclude_event_by_id(event_id)
        if not event_id: raise HttpNotFoundError("Participante não encontrado")
        
        return HttpResponse(body=None, status_code= 200)
    
    def update_event(self, http_request: HttpRequest) -> HttpResponse:
        body = http_request.body
        event_id = http_request.param["event_id"]

        self.__events_repository.update_event_by_id(body, event_id)

        return HttpResponse(body=body, status_code= 201)