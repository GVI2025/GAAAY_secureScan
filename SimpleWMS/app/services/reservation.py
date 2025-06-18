from sqlalchemy.orm import Session
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate, ReservationUpdate
from datetime import date, time

def get_reservation(db: Session, reservation_id: str):
    return db.query(Reservation).filter(Reservation.id == reservation_id).first()

def list_reservations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Reservation).offset(skip).limit(limit).all()

def check_availability(db: Session, salle_id: str, date_reservation: date, heure_reservation: time):
    """Check if a room is available at the given date and time"""
    existing = db.query(Reservation).filter(
        Reservation.salle_id == salle_id,
        Reservation.date == date_reservation,
        Reservation.heure == heure_reservation
    ).first()
    return existing is None

def create_reservation(db: Session, reservation: ReservationCreate):
    # Check availability before creating
    if not check_availability(db, reservation.salle_id, reservation.date, reservation.heure):
        raise ValueError("Cette salle est déjà réservée à ce créneau")
    
    db_reservation = Reservation(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def update_reservation(db: Session, reservation_id: str, reservation_data: ReservationUpdate):
    db_reservation = get_reservation(db, reservation_id)
    if db_reservation:
        # Check availability for the new slot if date/time changed
        if (reservation_data.salle_id != db_reservation.salle_id or 
            reservation_data.date != db_reservation.date or 
            reservation_data.heure != db_reservation.heure):
            if not check_availability(db, reservation_data.salle_id, reservation_data.date, reservation_data.heure):
                raise ValueError("Cette salle est déjà réservée à ce créneau")
        
        for key, value in reservation_data.dict().items():
            setattr(db_reservation, key, value)
        db.commit()
        db.refresh(db_reservation)
    return db_reservation

def delete_reservation(db: Session, reservation_id: str):
    db_reservation = get_reservation(db, reservation_id)
    if db_reservation:
        db.delete(db_reservation)
        db.commit()
    return db_reservation