from fastapi import FastAPI
from src.api.routers import jira_router
from src.api.routers.activity_router import router as activity_router
from src.api.routers.github_router import router as github_router

from src.core.logger import get_logger
from src.core.config import settings

logger = get_logger(__name__)

app = FastAPI(
    title="Team Activity Monitor",
    description="AI agent integrating with JIRA and GitHub",
    version="1.0.0",
)

app.include_router(jira_router.router)
app.include_router(activity_router)

app.include_router(github_router)


@app.get("/health")
def health_check():
    return {"status": "ok", "environment": settings.env}
