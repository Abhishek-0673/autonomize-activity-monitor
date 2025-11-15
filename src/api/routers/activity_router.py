from fastapi import APIRouter
from src.api.models.query_models import QueryRequestModel
from src.services.query_parser_service import QueryParserService
from src.core.user_resolver import UserResolver
from src.services.jira_service import JiraService

router = APIRouter()

jira_service = JiraService()

@router.post("/activity")
def get_activity(payload: QueryRequestModel):
    question = payload.question

    user_name = QueryParserService.extract_user(question)
    if not user_name:
        return {"message": "Could not identify the user from your question."}

    account_id = UserResolver.resolve(user_name)
    if not account_id:
        return {"message": f"No accountId configured for '{user_name}'"}

    return jira_service.get_user_issues(account_id)
