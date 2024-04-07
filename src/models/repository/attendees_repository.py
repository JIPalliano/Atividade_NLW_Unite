# Arquivo que irá colocar dados no banco de dados storage, na tabela Events

from typing import Dict, List
from src.models.settings.connection import db_connection_handler
from src.models.entities.attendees import Attendees
from src.models.entities.check_ins import CheckIns
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from src.models.entities.events import Events
from src.errors.error_types.http_conflict import HttpConflictError

class AttendeesRepository:
#Criar prticipante em um evento
    def insert_attendees(self, attendeesInfo: Dict) -> Dict:
        with db_connection_handler as database:
            try:
                attendees = Attendees(
                    id = attendeesInfo.get("uuid"),
                    name = attendeesInfo.get("name"),
                    email = attendeesInfo.get("email"),
                    event_id = attendeesInfo.get("event_id"),
                )
                database.session.add(attendees)
                database.session.commit()
                
                return attendeesInfo
            
            except IntegrityError:
                raise HttpConflictError('Participante já foi cadastrado!')
            except Exception as exception:
                database.session.rollback()
                raise exception            
#consulta no banco    
    def get_attendees_by_id(self, attendees_id: str) -> Attendees:
        with db_connection_handler as database:
            try:
                attendees = (
                    database.session
                        .query(Attendees)
                        .join(Events, Events.id == Attendees.event_id)
                        .filter(Attendees.id == attendees_id)
                        .with_entities(
                            Attendees.name,
                            Attendees.email,
                            Events.title
                        )
                        .one()
                )
                return attendees
            except NoResultFound:
                return None
            
#consultar número de participantes no evento
    def get_attendees_by_event_id(self, event_id=str) -> List[Attendees]:
        with db_connection_handler as database:
            attendees = (
                database.session
                .query(Attendees)
                .outerjoin(CheckIns, CheckIns.attendeeId == Attendees.id)
                .filter(Attendees.event_id == event_id)
                .with_entities(
                    Attendees.id,
                    Attendees.name,
                    Attendees.email,
                    CheckIns.created_at.label("checkedInAt"),
                    Attendees.created_at.label("createdAt")
                )
                .all()
            )
            return attendees
        
#excluir
    def exclude_attendees_by_id (self, attendees_id: str) -> Attendees:
        with db_connection_handler as database:
            try:
                attendees = (
                    database.session
                    .query(Attendees)
                    .filter(Attendees.id == attendees_id)
                    .delete()
                )
                database.session.commit()
                
                return attendees
                
            except NoResultFound:
                return None

#Atualizar dados do participante
    def update_attendees_by_id(self, attendeesupdate: Dict, attendees_id: str) -> Attendees:
        with db_connection_handler as database:
            try:
                attendees = (database.session
                .query(Attendees)
                .filter(Attendees.id == attendees_id)
                .first()
                )
                if Attendees:
                    attendees.name = attendeesupdate["name"] if attendeesupdate["name"] else Attendees.name
                    attendees.email = attendeesupdate["email"] if attendeesupdate["email"] else Attendees.email
                    
                else:
                    return None
                    
                database.session.commit()
                
                return attendeesupdate
            
            except AttributeError:
                raise HttpConflictError('Participante não encontrado!')
            except IntegrityError:
                raise HttpConflictError('Participante não encontrado!')
            except Exception as exception:
                database.session.rollback()
                raise exception     