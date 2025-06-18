from sqlalchemy.orm import Session
from app.models import Implantation as ImplantationModel
from app.schemas.implantation import ImplantationCreate, ImplantationUpdate

def get_implantation(db: Session, implantation_id: str):
    return db.query(ImplantationModel).filter(ImplantationModel.id == implantation_id).first()

def list_implantations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ImplantationModel).offset(skip).limit(limit).all()

def create_implantation(db: Session, implantation: ImplantationCreate):
    db_implantation = ImplantationModel(**implantation.dict())
    db.add(db_implantation)
    db.commit()
    db.refresh(db_implantation)
    return db_implantation

def update_implantation(db: Session, implantation_id: str, implantation_data: ImplantationUpdate):
    db_implantation = get_implantation(db, implantation_id)
    if db_implantation:
        for key, value in implantation_data.dict().items():
            setattr(db_implantation, key, value)
        db.commit()
        db.refresh(db_implantation)
    return db_implantation

def delete_implantation(db: Session, implantation_id: str):
    db_implantation = get_implantation(db, implantation_id)
    if db_implantation:
        db.delete(db_implantation)
        db.commit()
    return db_implantation
