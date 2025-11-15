class ActivitySummaryService:
    @staticmethod
    def generate(user: str, jira_data: dict, github_data: dict) -> str:
        """
        Human-friendly summary about user's activity.
        """

        # Extract JIRA info
        jira_count = jira_data.get("meta", {}).get("total", 0)

        # Extract GitHub info
        commit_count = github_data.get("commit_meta", {}).get("total", 0)
        pr_count = github_data.get("pr_meta", {}).get("total", 0)
        repo_count = github_data.get("repo_meta", {}).get("total", 0)

        parts = []

        # JIRA
        if jira_count > 0:
            parts.append(f"has {jira_count} active JIRA issue(s)")
        else:
            parts.append("has no active JIRA issues")

        # Commits
        if commit_count > 0:
            parts.append(f"made {commit_count} commit(s)")
        else:
            parts.append("made no recent commits")

        # PRs
        if pr_count > 0:
            parts.append(f"opened {pr_count} pull request(s)")
        else:
            parts.append("opened no recent pull requests")

        # Repos
        if repo_count > 0:
            parts.append(f"worked in {repo_count} repositories recently")
        else:
            parts.append("has not been active in GitHub repos recently")

        # Build final sentence
        summary = (
            f"Summary: In the recent period, {user} "
            + ", ".join(parts[:-1])
            + f", and {parts[-1]}."
        )

        return summary
