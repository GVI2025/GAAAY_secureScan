from sqlalchemy import Column, String, Float, Date, Enum
from uuid import uuid4
import enum

from app.database.database import Base

class CategorieArticle(enum.Enum):
    PRODUIT = "Produit fini"
    PIECE = "Pièce détachée"
    CONSOMMABLE = "Consommable"

class Article(Base):
    __tablename__ = "articles"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    sku = Column(String, unique=True, nullable=False)
    designation = Column(String, nullable=False)
    categorie = Column(Enum(CategorieArticle), nullable=False)
    poids_kg = Column(Float, nullable=False)
    volume_m3 = Column(Float, nullable=False)
    date_peremption = Column(Date, nullable=True)
