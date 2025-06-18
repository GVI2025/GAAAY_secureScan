from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.reservation import ReservationRead, ReservationCreate, ReservationUpdate
from app.services import reservation as reservation_service
from app.database.database import get_db

router = APIRouter(prefix="/reservations", tags=["Réservations"])

@router.get("/", response_model=List[ReservationRead])
def list_reservations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return reservation_service.list_reservations(db, skip, limit)

@router.post("/", response_model=ReservationRead)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    try:
        return reservation_service.create_reservation(db, reservation)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{reservation_id}", response_model=ReservationRead)
def get_reservation(reservation_id: str, db: Session = Depends(get_db)):
    reservation = reservation_service.get_reservation(db, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Réservation non trouvée")
    return reservation

@router.put("/{reservation_id}", response_model=ReservationRead)
def update_reservation(reservation_id: str, reservation: ReservationUpdate, db: Session = Depends(get_db)):
    try:
        updated = reservation_service.update_reservation(db, reservation_id, reservation)
        if not updated:
            raise HTTPException(status_code=404, detail="Réservation non trouvée")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{reservation_id}", response_model=ReservationRead)
def delete_reservation(reservation_id: str, db: Session = Depends(get_db)):
    deleted = reservation_service.delete_reservation(db, reservation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Réservation non trouvée")
    return deleted
