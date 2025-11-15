from pydantic import BaseModel

class QueryRequestModel(BaseModel):
    question: str
