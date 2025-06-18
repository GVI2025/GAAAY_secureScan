from sqlalchemy import Column, String, Enum, ForeignKey, Table, Integer
from sqlalchemy.orm import relationship
from uuid import uuid4
import enum

from app.database.database import Base

class EtatCommande(enum.Enum):
    BROUILLON = "Brouillon"
    RESERVEE = "Réservée"
    PREPAREE = "Préparée"
    EXPEDIEE = "Expédiée"
    ANNULEE = "Annulée"

class Commande(Base):
    __tablename__ = "commandes"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    reference = Column(String, unique=True, nullable=False)
    etat = Column(Enum(EtatCommande), nullable=False)

    lignes = relationship("LigneCommande", back_populates="commande")

class LigneCommande(Base):
    __tablename__ = "lignes_commandes"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    commande_id = Column(String, ForeignKey("commandes.id"))
    article_id = Column(String, ForeignKey("articles.id"))
    quantite = Column(Integer, nullable=False)

    commande = relationship("Commande", back_populates="lignes")
    article = relationship("Article")
