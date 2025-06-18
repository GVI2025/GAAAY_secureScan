from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime

from app.database.database import Base

class Reception(Base):
    __tablename__ = "receptions"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    article_id = Column(String, ForeignKey("articles.id"), nullable=False)
    quantite = Column(Integer, nullable=False)
    fournisseur = Column(String, nullable=False)
    date_reception = Column(DateTime, default=datetime.utcnow)
    emplacement_id = Column(String, ForeignKey("emplacements.id"), nullable=False)

    article = relationship("Article")
    emplacement = relationship("Emplacement")
