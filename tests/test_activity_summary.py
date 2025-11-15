from src.services.activity_summary_service import ActivitySummaryService

def make_jira_resp(count):
    return {"data": {"items": [{"key":"k"}]*count, "meta": {"total": count}}}

def make_github_resp(commits, prs, repos):
    return {
        "commits": {"data": {"items": [{}]*commits, "meta": {"total": commits}}},
        "prs": {"data": {"items": [{}]*prs, "meta": {"total": prs}}},
        "recent_repos": {"data": {"items": [{}]*repos, "meta": {"total": repos}}}
    }

def test_summary_all_zero():
    sum_text = ActivitySummaryService.generate("abhishek", {"data": {"items": [], "meta": {"total": 0}}}, {
        "commits": {"data": {"items": [], "meta": {"total": 0}}},
        "prs": {"data": {"items": [], "meta": {"total": 0}}},
        "recent_repos": {"data": {"items": [], "meta": {"total": 0}}}
    })
    assert "no active" in sum_text.lower() or "no active" in sum_text.lower()

def test_summary_counts():
    jira = make_jira_resp(2)
    gh = make_github_resp(5, 1, 3)
    s = ActivitySummaryService.generate("abhishek", jira, gh)
    assert "2" in s or "2 active" in s
    assert "5" in s
    assert "1" in s
