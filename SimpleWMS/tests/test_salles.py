import pytest
from fastapi.testclient import TestClient

def test_create_salle(client: TestClient, sample_salle):
    """Test creation of a new salle"""
    response = client.post("/salles/", json=sample_salle)
    assert response.status_code == 200
    data = response.json()
    assert data["nom"] == sample_salle["nom"]
    assert data["capacite"] == sample_salle["capacite"]
    assert data["localisation"] == sample_salle["localisation"]
    assert data["disponible"] == sample_salle["disponible"]
    assert "id" in data

def test_create_salle_duplicate_name(client: TestClient, sample_salle):
    """Test that creating a salle with duplicate name fails"""
    # Create first salle
    client.post("/salles/", json=sample_salle)
    
    # Try to create second salle with same name
    response = client.post("/salles/", json=sample_salle)
    assert response.status_code == 400
    assert "Une salle avec ce nom existe déjà" in response.json()["detail"]

def test_get_salle(client: TestClient, sample_salle):
    """Test retrieving a specific salle"""
    # Create salle
    create_response = client.post("/salles/", json=sample_salle)
    salle_id = create_response.json()["id"]
    
    # Get salle
    response = client.get(f"/salles/{salle_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == salle_id
    assert data["nom"] == sample_salle["nom"]

def test_get_salle_not_found(client: TestClient):
    """Test retrieving non-existent salle"""
    response = client.get("/salles/nonexistent-id")
    assert response.status_code == 404
    assert "Salle non trouvée" in response.json()["detail"]

def test_list_salles(client: TestClient, sample_salle):
    """Test listing all salles"""
    # Create multiple salles
    salle1 = sample_salle.copy()
    salle1["nom"] = "Salle A"
    salle2 = sample_salle.copy()
    salle2["nom"] = "Salle B"
    
    client.post("/salles/", json=salle1)
    client.post("/salles/", json=salle2)
    
    # List salles
    response = client.get("/salles/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    names = [salle["nom"] for salle in data]
    assert "Salle A" in names
    assert "Salle B" in names

def test_list_salles_filter_disponible(client: TestClient, sample_salle):
    """Test filtering salles by availability"""
    # Create available salle
    salle_disponible = sample_salle.copy()
    salle_disponible["nom"] = "Salle Disponible"
    salle_disponible["disponible"] = True
    
    # Create unavailable salle
    salle_indisponible = sample_salle.copy()
    salle_indisponible["nom"] = "Salle Indisponible"
    salle_indisponible["disponible"] = False
    
    client.post("/salles/", json=salle_disponible)
    client.post("/salles/", json=salle_indisponible)
    
    # Filter available salles
    response = client.get("/salles/?disponible=true")
    assert response.status_code == 200
    data = response.json()
    for salle in data:
        assert salle["disponible"] is True
    
    # Filter unavailable salles
    response = client.get("/salles/?disponible=false")
    assert response.status_code == 200
    data = response.json()
    for salle in data:
        assert salle["disponible"] is False

def test_update_salle(client: TestClient, sample_salle):
    """Test updating a salle"""
    # Create salle
    create_response = client.post("/salles/", json=sample_salle)
    salle_id = create_response.json()["id"]
    
    # Update salle
    updated_data = sample_salle.copy()
    updated_data["capacite"] = 20
    updated_data["disponible"] = False
    
    response = client.put(f"/salles/{salle_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["capacite"] == 20
    assert data["disponible"] is False

def test_update_salle_not_found(client: TestClient, sample_salle):
    """Test updating non-existent salle"""
    response = client.put("/salles/nonexistent-id", json=sample_salle)
    assert response.status_code == 404
    assert "Salle non trouvée" in response.json()["detail"]

def test_delete_salle(client: TestClient, sample_salle):
    """Test deleting a salle"""
    # Create salle
    create_response = client.post("/salles/", json=sample_salle)
    salle_id = create_response.json()["id"]
    
    # Delete salle
    response = client.delete(f"/salles/{salle_id}")
    assert response.status_code == 200
    
    # Verify deletion
    get_response = client.get(f"/salles/{salle_id}")
    assert get_response.status_code == 404

def test_delete_salle_not_found(client: TestClient):
    """Test deleting non-existent salle"""
    response = client.delete("/salles/nonexistent-id")
    assert response.status_code == 404
    assert "Salle non trouvée" in response.json()["detail"]
