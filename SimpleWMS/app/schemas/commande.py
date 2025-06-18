from pydantic import BaseModel
from enum import Enum
from typing import List

class EtatCommande(str, Enum):
    BROUILLON = "Brouillon"
    RESERVEE = "Réservée"
    PREPAREE = "Préparée"
    EXPEDIEE = "Expédiée"
    ANNULEE = "Annulée"

class LigneCommandeBase(BaseModel):
    article_id: str
    quantite: int

class LigneCommandeCreate(LigneCommandeBase):
    pass

class LigneCommandeRead(LigneCommandeBase):
    id: str

    class Config:
        orm_mode = True

class CommandeBase(BaseModel):
    reference: str
    etat: EtatCommande

class CommandeCreate(CommandeBase):
    lignes: List[LigneCommandeCreate]

class CommandeUpdate(CommandeBase):
    pass

class CommandeRead(CommandeBase):
    id: str
    lignes: List[LigneCommandeRead]

    class Config:
        orm_mode = True
