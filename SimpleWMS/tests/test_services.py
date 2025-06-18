import pytest
from datetime import date, time
from app.services import salle as salle_service
from app.services import reservation as reservation_service
from app.schemas.salle import SalleCreate
from app.schemas.reservation import ReservationCreate

def test_salle_service_create(db_session):
    """Test salle service creation"""
    salle_data = SalleCreate(
        nom="Test Salle",
        capacite=15,
        localisation="Test Location",
        disponible=True
    )
    
    created_salle = salle_service.create_salle(db_session, salle_data)
    assert created_salle.nom == "Test Salle"
    assert created_salle.capacite == 15
    assert created_salle.disponible is True

def test_salle_service_filter_by_availability(db_session):
    """Test filtering salles by availability"""
    # Create available salle
    salle1 = SalleCreate(nom="Salle Disponible", capacite=10, localisation="Loc1", disponible=True)
    salle_service.create_salle(db_session, salle1)
    
    # Create unavailable salle
    salle2 = SalleCreate(nom="Salle Indisponible", capacite=10, localisation="Loc2", disponible=False)
    salle_service.create_salle(db_session, salle2)
    
    # Test filtering
    available_salles = salle_service.list_salles(db_session, disponible=True)
    unavailable_salles = salle_service.list_salles(db_session, disponible=False)
    
    assert all(salle.disponible for salle in available_salles)
    assert all(not salle.disponible for salle in unavailable_salles)

def test_reservation_service_availability_check(db_session):
    """Test reservation availability checking"""
    # Create salle
    salle_data = SalleCreate(nom="Test Salle", capacite=10, localisation="Test", disponible=True)
    salle = salle_service.create_salle(db_session, salle_data)
    
    test_date = date(2025, 1, 15)
    test_time = time(14, 0)
    
    # Initially should be available
    assert reservation_service.check_availability(db_session, salle.id, test_date, test_time) is True
    
    # Create reservation
    reservation_data = ReservationCreate(
        salle_id=salle.id,
        date=test_date,
        heure=test_time,
        utilisateur="test@example.com"
    )
    reservation_service.create_reservation(db_session, reservation_data)
    
    # Now should not be available
    assert reservation_service.check_availability(db_session, salle.id, test_date, test_time) is False

def test_reservation_service_conflict_prevention(db_session):
    """Test that conflicting reservations are prevented"""
    # Create salle
    salle_data = SalleCreate(nom="Test Salle", capacite=10, localisation="Test", disponible=True)
    salle = salle_service.create_salle(db_session, salle_data)
    
    test_date = date(2025, 1, 15)
    test_time = time(14, 0)
    
    # Create first reservation
    reservation1_data = ReservationCreate(
        salle_id=salle.id,
        date=test_date,
        heure=test_time,
        utilisateur="user1@example.com"
    )
    reservation_service.create_reservation(db_session, reservation1_data)
    
    # Try to create conflicting reservation
    reservation2_data = ReservationCreate(
        salle_id=salle.id,
        date=test_date,
        heure=test_time,
        utilisateur="user2@example.com"
    )
    
    with pytest.raises(ValueError, match="Cette salle est déjà réservée à ce créneau"):
        reservation_service.create_reservation(db_session, reservation2_data)
