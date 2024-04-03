from src.models.settings.connection import db_connection_handler
from src.models.entities.check_ins import CheckIns
from sqlalchemy.exc import IntegrityError

class CheckInRepository:
    def insert_check_in(self, attendees_id):
        with db_connection_handler as database:
            try:
                check_in = (
                    CheckIns(attendees_id=attendees_id)
                )
                database.session.add(check_in)
                database.session.commit()
                
                return attendees_id
            except IntegrityError:
                raise Exception(" Check In já cadastrado!")
            
            except Exception as exception:
                database.session.rollback()
                raise exception