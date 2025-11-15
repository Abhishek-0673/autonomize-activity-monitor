import pytest
from datetime import datetime, timezone
from src.services.github_service import GitHubService


@pytest.fixture
def gh_service():
    return GitHubService()


def fake_commit(timestamp):
    return {
        "sha": "abc123",
        "html_url": "http://example.com",
        "commit": {
            "author": {"date": timestamp},
            "message": "fix"
        }
    }


def test_get_commits_basic(mocker, gh_service):
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    commits = [fake_commit(now.isoformat()) for _ in range(8)]

    mocker.patch.object(
        gh_service.client,
        "get_recent_commits",
        return_value={"success": True, "data": commits},
    )

    res = gh_service.get_user_commits("user1", limit=5, offset=0)

    assert res["success"] is True
    assert "data" in res
    assert "items" in res["data"]
    assert len(res["data"]["items"]) == 5
    assert "meta" in res["data"]  # <- now checking inside data only
    meta = res["data"]["meta"]
    assert meta["returned"] == 5
    assert meta["total"] == 8


def test_get_commits_date_filter(mocker, gh_service):
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    old = now.replace(year=2000).isoformat()
    recent = now.isoformat()

    commits = [fake_commit(old), fake_commit(recent)]

    mocker.patch.object(
        gh_service.client,
        "get_recent_commits",
        return_value={"success": True, "data": commits},
    )

    since_dt = now.replace(year=2020).isoformat()

    # your current service only supports `since`, not `date_from`
    res = gh_service.get_user_commits("user1", since=since_dt)

    assert res["success"] is True
    items = res["data"]["items"]
    assert len(items) == 1  # only the recent one
    assert items[0]["timestamp"] == recent


def test_get_prs_and_repos(mocker, gh_service):
    mocker.patch.object(
        gh_service.client,
        "get_pull_requests",
        return_value={
            "success": True,
            "data": {"items": [{"title": "PR1", "html_url": "http://pr"}]}
        },
    )

    mocker.patch.object(
        gh_service.client,
        "get_recent_repos",
        return_value={
            "success": True,
            "data": [{"name": "repo1"}]
        },
    )

    prs = gh_service.get_user_prs("user1")
    repos = gh_service.get_recent_repos("user1")

    assert prs["success"] is True
    assert repos["success"] is True

    assert prs["data"]["items"][0]["title"] == "PR1"
    assert repos["data"]["items"][0]["name"] == "repo1"
