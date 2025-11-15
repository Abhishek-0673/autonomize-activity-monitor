class ActivitySummaryService:
    """Activity summary generator."""
    @staticmethod
    def generate(user: str, jira_data: dict, github_data: dict) -> str:
        """
        Generates a clean, emoji-friendly, human readable activity summary.
        """

        def pluralize(count, noun):
            """Pluralize a noun based on count."""
            # handle nouns ending with 'y' -> 'ies' (repository -> repositories)
            if count == 0:
                return f"No {noun}s" if not noun.endswith("y") else f"No {noun[:-1]}ies"
            if count == 1:
                return f"1 {noun}"
            # plural form
            if noun.endswith("y"):
                return f"{count} {noun[:-1]}ies"
            return f"{count} {noun}s"

        # JIRA
        jira_total = jira_data.get("meta", {}).get("total", 0)
        jira_line = (
            f"• {pluralize(jira_total, 'active issue')}"
            if jira_total > 0 else
            "• No active issues"
        )

        # COMMITS
        commit_total = github_data.get("commits", {}).get("meta", {}).get("total", 0)
        commit_line = (
            f"• {pluralize(commit_total, 'recent commit')}"
            if commit_total > 0 else
            "• No recent commits"
        )

        # PRS
        pr_total = github_data.get("prs", {}).get("meta", {}).get("total", 0)
        pr_line = (
            f"• {pluralize(pr_total, 'active pull request')}"
            if pr_total > 0 else
            "• No active pull requests"
        )

        # REPOS
        repo_total = github_data.get("recent_repos", {}).get("meta", {}).get("total", 0)
        repo_line = (
            f"• Active in {pluralize(repo_total, 'repository')}"
            if repo_total > 0 else
            "• No recent repository activity"
        )

        # Final nicely formatted summary
        return (
            f"👤 **Activity Summary for {user.capitalize()}**\n\n"
            f"🧩 **JIRA**\n{jira_line}\n\n"
            f"💻 **Commits**\n{commit_line}\n\n"
            f"📂 **Pull Requests**\n{pr_line}\n\n"
            f"📦 **Repositories**\n{repo_line}"
        )
