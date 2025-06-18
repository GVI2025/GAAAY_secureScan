from sqlalchemy import Column, String, Float, Enum
from uuid import uuid4
import enum

from app.database.database import Base

class TypeEmplacement(enum.Enum):
    STOCKAGE = "Zone de stockage"
    VENTE = "Surface de vente"
    RESERVATION = "Zone de réservation"
    RECEPTION = "Réception"
    EXPEDITION = "Expédition"

class Emplacement(Base):
    __tablename__ = "emplacements"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    code = Column(String, unique=True, nullable=False)
    type = Column(Enum(TypeEmplacement), nullable=False)
    capacite_poids_kg = Column(Float, nullable=False)
    capacite_volume_m3 = Column(Float, nullable=False)
