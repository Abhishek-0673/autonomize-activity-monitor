from src.api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_github_api():
    res = client.get("/github/torvalds")  # should work for demo
    assert res.status_code == 200
