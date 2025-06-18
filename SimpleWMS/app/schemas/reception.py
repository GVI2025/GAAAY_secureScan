from pydantic import BaseModel
from datetime import datetime

class ReceptionBase(BaseModel):
    article_id: str
    quantite: int
    fournisseur: str
    date_reception: datetime
    emplacement_id: str

class ReceptionCreate(ReceptionBase):
    pass

class ReceptionUpdate(ReceptionBase):
    pass

class ReceptionRead(ReceptionBase):
    id: str

    class Config:
        orm_mode = True
