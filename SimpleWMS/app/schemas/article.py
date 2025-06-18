from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum

class CategorieArticle(str, Enum):
    PRODUIT = "Produit fini"
    PIECE = "Pièce détachée"
    CONSOMMABLE = "Consommable"

class ArticleBase(BaseModel):
    sku: str
    designation: str
    categorie: CategorieArticle
    poids_kg: float
    volume_m3: float
    date_peremption: Optional[date] = None

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(ArticleBase):
    pass

class ArticleRead(ArticleBase):
    id: str

    class Config:
        orm_mode = True
