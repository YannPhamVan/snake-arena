from fastapi.testclient import TestClient

def test_root(client: TestClient):
    response = client.get("/api")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Snake Arena API"}
