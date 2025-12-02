import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.mock_db import mock_db

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    mock_db.reset()
    yield
    mock_db.reset()
