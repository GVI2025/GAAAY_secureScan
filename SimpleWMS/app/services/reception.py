from sqlalchemy.orm import Session
from app.models import Reception as ReceptionModel
from app.schemas.reception import ReceptionCreate, ReceptionUpdate

def get_reception(db: Session, reception_id: str):
    return db.query(ReceptionModel).filter(ReceptionModel.id == reception_id).first()

def list_receptions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ReceptionModel).offset(skip).limit(limit).all()

def create_reception(db: Session, reception: ReceptionCreate):
    db_reception = ReceptionModel(**reception.dict())
    db.add(db_reception)
    db.commit()
    db.refresh(db_reception)
    return db_reception

def update_reception(db: Session, reception_id: str, reception_data: ReceptionUpdate):
    db_reception = get_reception(db, reception_id)
    if db_reception:
        for key, value in reception_data.dict().items():
            setattr(db_reception, key, value)
        db.commit()
        db.refresh(db_reception)
    return db_reception

def delete_reception(db: Session, reception_id: str):
    db_reception = get_reception(db, reception_id)
    if db_reception:
        db.delete(db_reception)
        db.commit()
    return db_reception
