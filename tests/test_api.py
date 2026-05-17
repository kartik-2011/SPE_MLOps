from fastapi.testclient import TestClient

from app.main import app
from app.model_loader import resolve_project_path
from training.registry import get_current_model_entry
from training.train import train_model


def ensure_model():
    entry = get_current_model_entry()
    if entry is None:
        train_model(data_source="demo")
        return
    artifact_path = resolve_project_path(entry["artifact_path"])
    if not artifact_path.exists():
        train_model(data_source="demo")


def test_health_endpoint():
    ensure_model()
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_homepage_renders():
    ensure_model()
    with TestClient(app) as client:
        response = client.get("/")
    assert response.status_code == 200
    assert "House Price Prediction System" in response.text


def test_predict_endpoint():
    ensure_model()
    payload = {
        "MedInc": 8.3252,
        "HouseAge": 41.0,
        "AveRooms": 6.984127,
        "AveBedrms": 1.02381,
        "Population": 322.0,
        "AveOccup": 2.555556,
        "Latitude": 37.88,
        "Longitude": -122.23,
    }
    with TestClient(app) as client:
        response = client.post("/predict", json=payload)
    body = response.json()
    assert response.status_code == 200
    assert body["model_version"].startswith("v")
    assert isinstance(body["prediction"], float)
