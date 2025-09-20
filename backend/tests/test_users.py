import pytest
from fastapi.testclient import TestClient
from backend_backup.main import app

client = TestClient(app)

def test_read_users():
    response = client.get("/api/users/")
    assert response.status_code == 200