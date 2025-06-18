from pydantic import BaseModel
from enum import Enum
from typing import Optional

class TypeEmplacement(str, Enum):
    STOCKAGE = "Zone de stockage"
    VENTE = "Surface de vente"
    RESERVATION = "Zone de réservation"
    RECEPTION = "Réception"
    EXPEDITION = "Expédition"

class EmplacementBase(BaseModel):
    code: str
    type: TypeEmplacement
    capacite_poids_kg: float
    capacite_volume_m3: float

class EmplacementCreate(EmplacementBase):
    pass

class EmplacementUpdate(EmplacementBase):
    pass

class EmplacementRead(EmplacementBase):
    id: str

    class Config:
        orm_mode = True
