from sqlalchemy.orm import Session
from app.models import Emplacement as EmplacementModel
from app.schemas.emplacement import EmplacementCreate, EmplacementUpdate

def get_emplacement(db: Session, emplacement_id: str):
    return db.query(EmplacementModel).filter(EmplacementModel.id == emplacement_id).first()

def get_emplacement_by_code(db: Session, code: str):
    return db.query(EmplacementModel).filter(EmplacementModel.code == code).first()

def list_emplacements(db: Session, skip: int = 0, limit: int = 100):
    return db.query(EmplacementModel).offset(skip).limit(limit).all()

def create_emplacement(db: Session, emplacement: EmplacementCreate):
    db_emplacement = EmplacementModel(**emplacement.dict())
    db.add(db_emplacement)
    db.commit()
    db.refresh(db_emplacement)
    return db_emplacement

def update_emplacement(db: Session, emplacement_id: str, emplacement_data: EmplacementUpdate):
    db_emplacement = get_emplacement(db, emplacement_id)
    if db_emplacement:
        for key, value in emplacement_data.dict().items():
            setattr(db_emplacement, key, value)
        db.commit()
        db.refresh(db_emplacement)
    return db_emplacement

def delete_emplacement(db: Session, emplacement_id: str):
    db_emplacement = get_emplacement(db, emplacement_id)
    if db_emplacement:
        db.delete(db_emplacement)
        db.commit()
    return db_emplacement
