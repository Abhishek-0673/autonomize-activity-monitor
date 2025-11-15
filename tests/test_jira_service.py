# tests/test_jira_service.py
import pytest
from src.services.jira_service import JiraService

@pytest.fixture
def jira_service():
    return JiraService()


def make_issue(key):
    return {
        "key": key,
        "fields": {
            "summary": "task",
            "status": {"name": "To Do"},
            "updated": "2025-11-12T00:00:00.000+0530"
        }
    }


def test_get_user_issues_success(mocker, jira_service):
    # Prepare fake issues
    issues = [make_issue("SCRUM-1"), make_issue("SCRUM-2")]

    # Mock client response
    mocker.patch.object(
        jira_service.client,
        "get_user_activity",
        return_value={"issues": issues, "count": 2}
    )

    res = jira_service.get_user_issues("5b4deb")

    # Validate new response shape
    assert res["success"] is True
    assert "data" in res

    data = res["data"]
    assert isinstance(data["items"], list)
    assert len(data["items"]) == 2
    assert data["items"][0]["key"] == "SCRUM-1"

    # Meta block
    assert "meta" in data
    assert data["meta"]["total"] == 2
    assert data["meta"]["returned"] == 2


def test_get_user_issues_empty(mocker, jira_service):
    mocker.patch.object(
        jira_service.client,
        "get_user_activity",
        return_value={"issues": [], "count": 0}
    )

    res = jira_service.get_user_issues("5b4deb")

    # Should still be success but with message
    assert "message" in res
    assert "No active issues" in res["message"]

def test_issue_details_parsing(mocker, jira_service):
    raw = {
        "key": "SCRUM-2",
        "fields": {
            "summary": "Task 2",
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {"type": "paragraph", "content": [{"type": "text", "text": "Hello world"}]}
                ]
            },
            "status": {"name": "In Progress"},
            "priority": {"name": "Medium"},
            "assignee": {"displayName": "AbhiAlien"},
            "reporter": {"displayName": "Reporter"},
            "created": "2025-11-12T20:44:16.019+0530",
            "updated": "2025-11-12T20:44:16.558+0530",
            "labels": []
        },
        "changelog": [
            {
                "field": "status",
                "from": "To Do",
                "to": "In Progress",
                "created": "2025-11-12T20:44:16.558+0530"
            }
        ]
    }

    mocker.patch.object(jira_service.client, "get_issue_details", return_value=raw)

    res = jira_service.get_issue_details("SCRUM-2")

    assert res["success"] is True
    assert "data" in res
    assert "items" in res["data"]

    data = res["data"]["items"]   # ⭐ FIXED LINE

    assert data["summary"] == "Task 2"
    assert data["description"] == "Hello world"
    assert data["status"] == "In Progress"
    assert data["priority"] == "Medium"
    assert data["assignee"] == "AbhiAlien"
    assert data["reporter"] == "Reporter"

    assert len(data["changelog"]) == 1
    change = data["changelog"][0]
    assert change["field"] == "status"
    assert change["from"] == "To Do"
    assert change["to"] == "In Progress"

