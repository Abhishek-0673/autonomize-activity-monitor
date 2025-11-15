import os
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")


class Settings(BaseSettings):
    """Application settings."""
    jira_base_url: str = ""
    jira_email: str = ""
    jira_api_token: str = ""
    jira_abhishek_account_id: str = ""
    jira_abhialien_account_id: str = ""
    jira_test_account_id: str = ""
    github_token: str = ""
    github_repo_name: str = ""
    github_username_for_abhishek: str = ""
    github_username_for_abhialien: str = ""
    github_api_host_url: str = ""
    openai_api_key: str = ""
    use_mock_data: bool = False
    env: str = "development"

    model_config = SettingsConfigDict(env_file=ENV_PATH)

settings = Settings()
