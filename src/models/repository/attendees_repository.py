# Arquivo que irá colocar dados no banco de dados storage, na tabela Events

from typing import Dict, List
from src.models.settings.connection import db_connection_handler
from src.models.entities.attendees import Attendees
from src.models.entities.check_ins import CheckIns
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from src.models.entities.events import Events

class AttendeesRepository:
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
                raise Exception('Participante já foi cadastrado!')
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