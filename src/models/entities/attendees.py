# Realizando a declaração da tabela "attendees" que esta 
# no banco de dados
from src.models.settings.base import Base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func

#classe que esta referenciando a tabela
class Attendees(Base):
    __tablename__ = "attendees"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    event_id = Column(String, ForeignKey("events.id"))
    created_at = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"Attendees [Name={self.name}, E-mail={self.email}], Event_id={self.event_id}"