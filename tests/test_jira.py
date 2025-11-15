import os

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_jira_valid_user():
    ACCOUNT_ID = os.environ.get("JIRA_ABHISHEK_ACCOUNT_ID")
    res = client.get(f"/jira/{ACCOUNT_ID}")
    assert res.status_code == 200
    assert "message" in res.json()


def test_jira_invalid_user():
    res = client.get("/jira/invalid123")
    assert res.status_code == 200
    body = res.json()
    assert "error" in body or "message" in body
