from pydantic import BaseModel
from typing import Optional
from datetime import date, time

class ReservationBase(BaseModel):
    salle_id: str
    date: date
    heure: time
    utilisateur: str
    commentaire: Optional[str] = None

class ReservationCreate(ReservationBase):
    pass

class ReservationUpdate(ReservationBase):
    pass

class ReservationRead(ReservationBase):
    id: str

    class Config:
        orm_mode = True