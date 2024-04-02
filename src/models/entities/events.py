# Realizando a declaração da tabela "events" que esta 
# no banco de dados
from src.models.settings.base import Base
from sqlalchemy import Column, String, Integer

#clase que esta referenciando a tabela
class Events(Base):
    __tablename__ = "events"
    
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    details = Column(String)
    slug = Column(String, nullable=False)
    maximum_attendees = Column(Integer)