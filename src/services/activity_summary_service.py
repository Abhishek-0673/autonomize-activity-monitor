class ActivitySummaryService:
    """Deterministic summary generator (no AI)."""

    @staticmethod
    def generate(user: str, jira_data: dict, github_data: dict) -> str:
        """
        Creates a concise, emoji-friendly summary fully aligned with test expectations.
        """

        def extract_count(section: dict) -> int:
            """
            Tests expect:
            section["data"]["meta"]["total"]
            """
            return (
                section.get("data", {})
                       .get("meta", {})
                       .get("total", 0)
            )

        def pluralize(count: int, singular: str, plural: str = None):
            """
            Proper plural logic with human-readable forms.
            Automatically handles:
             - “issue/issues”
             - “commit/commits”
             - “repository/repositories”
            """
            if plural is None:
                if singular.endswith("y"):
                    plural = singular[:-1] + "ies"
                else:
                    plural = singular + "s"

            if count == 0:
                return f"No {plural}"
            if count == 1:
                return f"1 {singular}"
            return f"{count} {plural}"

        # Extract counts from normalized success() wrapper
        jira_total = extract_count(jira_data)
        commit_total = extract_count(github_data.get("commits", {}))
        pr_total = extract_count(github_data.get("prs", {}))
        repo_total = extract_count(github_data.get("recent_repos", {}))

        # Build sections
        jira_line = f"• {pluralize(jira_total, 'active issue')}"
        commit_line = f"• {pluralize(commit_total, 'recent commit')}"
        pr_line = f"• {pluralize(pr_total, 'active pull request')}"
        repo_line = f"• {pluralize(repo_total, 'repository', 'repositories')}"

        # Final output (tests allow emojis + markdown)
        return (
            f"👤 **Activity Summary for {user.capitalize()}**\n\n"
            f"🧩 **JIRA**\n{jira_line}\n\n"
            f"💻 **Commits**\n{commit_line}\n\n"
            f"📂 **Pull Requests**\n{pr_line}\n\n"
            f"📦 **Repositories**\n{repo_line}"
        )
