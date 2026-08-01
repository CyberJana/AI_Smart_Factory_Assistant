import os

os.environ["DATABASE_URL"] = "sqlite:///./test_factory.db"
os.environ["JWT_SECRET"] = "test-secret-with-at-least-thirty-two-characters"

from fastapi.testclient import TestClient

from app.db import Base, engine
from app.main import app


def test_health_check() -> None:
    with TestClient(app) as client:
        response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_authenticated_dashboard_and_copilot() -> None:
    Base.metadata.drop_all(bind=engine)
    with TestClient(app) as client:
        login = client.post(
            "/api/v1/auth/login",
            json={"email": "admin@smartfactory.example", "password": "ChangeMe123!"},
        )
        assert login.status_code == 200
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        dashboard = client.get("/api/v1/analytics/dashboard", headers=headers)
        assert dashboard.status_code == 200
        assert dashboard.json()["kpis"]["machine_count"] == 4

        answer = client.post(
            "/api/v1/chat",
            headers=headers,
            json={"question": "Which machine needs maintenance?"},
        )
        assert answer.status_code == 200
        assert "PRESS-02" in answer.json()["answer"]
