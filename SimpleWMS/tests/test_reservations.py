import pytest
from fastapi.testclient import TestClient

def test_create_reservation(client: TestClient, sample_salle, sample_reservation):
    """Test creation of a new reservation"""
    # Create salle first
    salle_response = client.post("/salles/", json=sample_salle)
    salle_id = salle_response.json()["id"]
    
    # Create reservation
    reservation_data = sample_reservation.copy()
    reservation_data["salle_id"] = salle_id
    
    response = client.post("/reservations/", json=reservation_data)
    assert response.status_code == 200
    data = response.json()
    assert data["salle_id"] == salle_id
    assert data["date"] == sample_reservation["date"]
    assert data["heure"] == sample_reservation["heure"]
    assert data["utilisateur"] == sample_reservation["utilisateur"]
    assert "id" in data

def test_create_reservation_conflict(client: TestClient, sample_salle, sample_reservation):
    """Test that creating conflicting reservations fails"""
    # Create salle
    salle_response = client.post("/salles/", json=sample_salle)
    salle_id = salle_response.json()["id"]
    
    # Create first reservation
    reservation_data = sample_reservation.copy()
    reservation_data["salle_id"] = salle_id
    response1 = client.post("/reservations/", json=reservation_data)
    assert response1.status_code == 200
    
    # Try to create conflicting reservation
    conflicting_reservation = reservation_data.copy()
    conflicting_reservation["utilisateur"] = "autre.utilisateur@example.com"
    
    response2 = client.post("/reservations/", json=conflicting_reservation)
    assert response2.status_code == 400
    assert "Cette salle est déjà réservée à ce créneau" in response2.json()["detail"]

def test_get_reservation(client: TestClient, sample_salle, sample_reservation):
    """Test retrieving a specific reservation"""
    # Create salle and reservation
    salle_response = client.post("/salles/", json=sample_salle)
    salle_id = salle_response.json()["id"]
    
    reservation_data = sample_reservation.copy()
    reservation_data["salle_id"] = salle_id
    create_response = client.post("/reservations/", json=reservation_data)
    reservation_id = create_response.json()["id"]
    
    # Get reservation
    response = client.get(f"/reservations/{reservation_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == reservation_id
    assert data["salle_id"] == salle_id

def test_get_reservation_not_found(client: TestClient):
    """Test retrieving non-existent reservation"""
    response = client.get("/reservations/nonexistent-id")
    assert response.status_code == 404
    assert "Réservation non trouvée" in response.json()["detail"]

def test_list_reservations(client: TestClient, sample_salle, sample_reservation):
    """Test listing all reservations"""
    # Create salle
    salle_response = client.post("/salles/", json=sample_salle)
    salle_id = salle_response.json()["id"]
    
    # Create multiple reservations
    reservation1 = sample_reservation.copy()
    reservation1["salle_id"] = salle_id
    reservation1["heure"] = "09:00:00"
    reservation1["utilisateur"] = "user1@example.com"
    
    reservation2 = sample_reservation.copy()
    reservation2["salle_id"] = salle_id
    reservation2["heure"] = "10:00:00"
    reservation2["utilisateur"] = "user2@example.com"
    
    client.post("/reservations/", json=reservation1)
    client.post("/reservations/", json=reservation2)
    
    # List reservations
    response = client.get("/reservations/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2

def test_update_reservation(client: TestClient, sample_salle, sample_reservation):
    """Test updating a reservation"""
    # Create salle and reservation
    salle_response = client.post("/salles/", json=sample_salle)
    salle_id = salle_response.json()["id"]
    
    reservation_data = sample_reservation.copy()
    reservation_data["salle_id"] = salle_id
    create_response = client.post("/reservations/", json=reservation_data)
    reservation_id = create_response.json()["id"]
    
    # Update reservation
    updated_data = reservation_data.copy()
    updated_data["heure"] = "15:00:00"
    updated_data["commentaire"] = "Réunion importante"
    
    response = client.put(f"/reservations/{reservation_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["heure"] == "15:00:00"
    assert data["commentaire"] == "Réunion importante"

def test_update_reservation_conflict(client: TestClient, sample_salle, sample_reservation):
    """Test updating reservation to conflicting slot fails"""
    # Create salle
    salle_response = client.post("/salles/", json=sample_salle)
    salle_id = salle_response.json()["id"]
    
    # Create two reservations
    reservation1_data = sample_reservation.copy()
    reservation1_data["salle_id"] = salle_id
    reservation1_data["heure"] = "09:00:00"
    create_response1 = client.post("/reservations/", json=reservation1_data)
    reservation1_id = create_response1.json()["id"]
    
    reservation2_data = sample_reservation.copy()
    reservation2_data["salle_id"] = salle_id
    reservation2_data["heure"] = "10:00:00"
    reservation2_data["utilisateur"] = "user2@example.com"
    client.post("/reservations/", json=reservation2_data)
    
    # Try to update first reservation to conflict with second
    updated_data = reservation1_data.copy()
    updated_data["heure"] = "10:00:00"
    
    response = client.put(f"/reservations/{reservation1_id}", json=updated_data)
    assert response.status_code == 400
    assert "Cette salle est déjà réservée à ce créneau" in response.json()["detail"]

def test_delete_reservation(client: TestClient, sample_salle, sample_reservation):
    """Test deleting a reservation"""
    # Create salle and reservation
    salle_response = client.post("/salles/", json=sample_salle)
    salle_id = salle_response.json()["id"]
    
    reservation_data = sample_reservation.copy()
    reservation_data["salle_id"] = salle_id
    create_response = client.post("/reservations/", json=reservation_data)
    reservation_id = create_response.json()["id"]
    
    # Delete reservation
    response = client.delete(f"/reservations/{reservation_id}")
    assert response.status_code == 200
    
    # Verify deletion
    get_response = client.get(f"/reservations/{reservation_id}")
    assert get_response.status_code == 404

def test_delete_reservation_not_found(client: TestClient):
    """Test deleting non-existent reservation"""
    response = client.delete("/reservations/nonexistent-id")
    assert response.status_code == 404
    assert "Réservation non trouvée" in response.json()["detail"]

def test_create_reservation_with_comment(client: TestClient, sample_salle, sample_reservation):
    """Test creating reservation with comment (v1.1.0 feature)"""
    # Create salle
    salle_response = client.post("/salles/", json=sample_salle)
    salle_id = salle_response.json()["id"]
    
    # Create reservation with comment
    reservation_data = sample_reservation.copy()
    reservation_data["salle_id"] = salle_id
    reservation_data["commentaire"] = "Réunion équipe dev"
    
    response = client.post("/reservations/", json=reservation_data)
    assert response.status_code == 200
    data = response.json()
    assert data["commentaire"] == "Réunion équipe dev"
