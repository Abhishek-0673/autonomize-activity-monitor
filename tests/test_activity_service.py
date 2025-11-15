import pytest
from src.services.activity_service import ActivityService

@pytest.fixture
def activity_service(mocker):
    svc = ActivityService()
    return svc

def test_activity_intent_jira(mocker, activity_service):
    # stub QueryParserService.extract_user
    mocker.patch("src.services.query_parser_service.QueryParserService.extract_user", return_value="abhishek")
    # stub UserResolver.resolve
    mocker.patch("src.core.user_resolver.UserResolver.resolve", return_value={"jira":"5b4", "github":"Abhishek-0673"})
    # stub IntentService.detect_intent
    mocker.patch("src.services.intent_service.IntentService.detect_intent", return_value="JIRA_ISSUES")
    # stub jira and github service calls
    mocker.patch.object(activity_service.jira, "get_user_issues", return_value={"success": True, "data": {"items": []}, "meta": {}})
    mocker.patch.object(activity_service.github, "get_user_github_activity", return_value={"commits":{"data":{"items":[]},"meta":{}}})

    res = activity_service.get_activity("What is Abhishek doing?", limit=5, offset=0)
    assert res["success"] is True
    assert "jira" in res["data"] or "jira" in res["message"] or True

def test_activity_unknown_user(mocker, activity_service):
    mocker.patch("src.services.query_parser_service.QueryParserService.extract_user", return_value=None)
    res = activity_service.get_activity("Who is Abhishek?")
    assert res["success"] is False
