import uuid
from src.models.repository.attendees_repository import AttendeesRepository
from src.models.repository.events_repository import EventsRepository
from src.http_types.http_request import HttpRequest
from src.http_types.http_response import HttpResponse
from src.errors.error_types.http_not_found import HttpNotFoundError
from src.errors.error_types.http_conflict import HttpConflictError


class AttendeesHandler:
    def __init__(self) -> None:
        self.__attendees_repository = AttendeesRepository()
        self.__events_repository = EventsRepository()
    
    #Registrando um participante em um evento    
    def registry(self, http_request: HttpRequest) -> HttpResponse:
        body = http_request.body
        event_id = http_request.param["event_id"]
        
        event_attendees_count = self.__events_repository.count_event_attendees(event_id)
        if(
            event_attendees_count["attendeesAmount"] and event_attendees_count["maximumAttendees"] < event_attendees_count["attendeesAmount"]
        ): raise HttpConflictError("Evento Lotado")
        
        body["uuid"] = str(uuid.uuid4())
        body["event_id"] = event_id
        self.__attendees_repository.insert_attendees(body)
        
        return HttpResponse(body=None, status_code= 201)
    
    #Mostrando o resultado 0 cartão de acesso de um participante
    def find_attendees_badge(self, http_request: HttpRequest) -> HttpResponse:
        attendees_id = http_request.param["attendees_id"]
        badge = self.__attendees_repository.get_attendees_by_id(attendees_id)
        if not badge: raise HttpNotFoundError("Participante não encontrado")
        
        return HttpResponse(
            body={
                "badge":{
                    "name": badge.name,
                    "email": badge.email,
                    "envenTilte": badge.title
                }
            },
            status_code = 200
        )
    
    #Mostrando o resultado de participantes em um evento    
    def find_attendees_from_event(self, http_request = HttpRequest) -> HttpResponse:
        event_id = http_request.param["event_id"]
        attendees = self.__attendees_repository.get_attendees_by_event_id(event_id)
        if not attendees: raise HttpNotFoundError("Participantes não encontrado")
        
        formatted_attendees = []
        for attendee in attendees:
            formatted_attendees.append(
                {
                    "id":attendee.id,
                    "name": attendee.name,
                    "email": attendee.email,
                    "checkInAt": attendee.checkedInAt,
                    "createdAt": attendee.createdAt
                }
            )
            
        return HttpResponse(
            body={"attendees": formatted_attendees},
            status_code=200
        )
        
    def exclude_attendees(self, http_request: HttpRequest) -> HttpResponse:
        attendees_id = http_request.param["attendees_id"]
        self.__attendees_repository.exclude_attendees_by_id(attendees_id)
        if not attendees_id: raise HttpNotFoundError("Participante não encontrado")
        
        return HttpResponse(body=None, status_code= 200)
    
    def update_attendees(self, http_request: HttpRequest) -> HttpResponse:
        body = http_request.body
        attendees_id = http_request.param["attendees_id"]

        self.__attendees_repository.update_attendees_by_id(body, attendees_id)

        return HttpResponse(body=body, status_code= 201)