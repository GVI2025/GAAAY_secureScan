from sqlalchemy.orm import Session
from app.models.salle import Salle
from app.schemas.salle import SalleCreate, SalleUpdate
from typing import Optional

def get_salle(db: Session, salle_id: str):
    return db.query(Salle).filter(Salle.id == salle_id).first()

def get_salle_by_nom(db: Session, nom: str):
    return db.query(Salle).filter(Salle.nom == nom).first()

def list_salles(db: Session, skip: int = 0, limit: int = 100, disponible: Optional[bool] = None):
    query = db.query(Salle)
    if disponible is not None:
        query = query.filter(Salle.disponible == disponible)
    return query.offset(skip).limit(limit).all()

def create_salle(db: Session, salle: SalleCreate):
    db_salle = Salle(**salle.dict())
    db.add(db_salle)
    db.commit()
    db.refresh(db_salle)
    return db_salle

def update_salle(db: Session, salle_id: str, salle_data: SalleUpdate):
    db_salle = get_salle(db, salle_id)
    if db_salle:
        for key, value in salle_data.dict().items():
            setattr(db_salle, key, value)
        db.commit()
        db.refresh(db_salle)
    return db_salle

def delete_salle(db: Session, salle_id: str):
    db_salle = get_salle(db, salle_id)
    if db_salle:
        db.delete(db_salle)
        db.commit()
    return db_salle
