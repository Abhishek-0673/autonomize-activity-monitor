class ActivitySummaryService:
    """Generates a readable dashboard-style summary."""

    @staticmethod
    def extract_count(section):
        """
        Extract meta.total from your unified API response:

        {
            "success": true,
            "message": "...",
            "data": {
                "items": {...},
                "meta": {...}
            }
        }
        """
        try:
            return section["data"]["items"]["meta"]["total"]
        except Exception:
            return 0

    @staticmethod
    def extract_github_count(section):
        """
        Extract meta.total for nested GitHub sections:

        github_data → data → items → commits → data → meta.total
        """
        try:
            return section["data"]["items"]["data"]["meta"]["total"]
        except Exception:
            return 0

    @staticmethod
    def generate(user: str, jira_data: dict, github_data: dict) -> str:

        # JIRA
        try:
            jira_total = jira_data["data"]["items"]["meta"]["total"]
        except Exception:
            jira_total = 0

        # COMMITS
        try:
            commit_total = github_data["data"]["items"]["commits"]["data"]["meta"]["total"]
        except Exception:
            commit_total = 0

        # PRS
        try:
            pr_total = github_data["data"]["items"]["prs"]["data"]["meta"]["total"]
        except Exception:
            pr_total = 0

        # REPOS
        try:
            repo_total = github_data["data"]["items"]["recent_repos"]["data"]["meta"]["total"]
        except Exception:
            repo_total = 0

        # Helpers
        def fmt(count, noun):
            if count == 0:
                return f"• No {noun}s"
            if count == 1:
                return f"• 1 {noun}"
            return f"• {count} {noun}s"

        # Build summary
        return (
            f"👤 **Activity Summary for {user.capitalize()}**\n\n"
            f"🧩 **JIRA**\n{fmt(jira_total, 'active issue')}\n\n"
            f"💻 **Commits**\n{fmt(commit_total, 'recent commit')}\n\n"
            f"📂 **Pull Requests**\n{fmt(pr_total, 'active pull request')}\n\n"
            f"📦 **Repositories**\n{fmt(repo_total, 'repository')}"
        )
