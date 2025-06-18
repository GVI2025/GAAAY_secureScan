from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship
from uuid import uuid4

from app.database.database import Base

class Salle(Base):
    __tablename__ = "salles"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    nom = Column(String, nullable=False)
    capacite = Column(Integer, nullable=False)
    localisation = Column(String, nullable=False)
    disponible = Column(Boolean, default=True)  # Added for v1.1.0

    # Relationship with reservations
    reservations = relationship("Reservation", back_populates="salle")
