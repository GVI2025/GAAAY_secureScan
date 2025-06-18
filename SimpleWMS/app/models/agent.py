from sqlalchemy import Column, String, Boolean
from uuid import uuid4

from app.database.database import Base

class Agent(Base):
    __tablename__ = "agents"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    nom = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    actif = Column(Boolean, default=True)
