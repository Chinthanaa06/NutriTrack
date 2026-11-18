from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_invalid_height_rejected():
    response = client.post("/api/assessments", json={
        "participant_code":"TEST-INVALID", "age_years":25, "sex_reference":"not_specified",
        "height_cm":0, "weight_kg":60
    })
    assert response.status_code == 422
