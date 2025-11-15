from src.services.query_parser_service import QueryParserService

def test_extract_user_basic():
    q = "What is Abhishek working on these days?"
    assert QueryParserService.extract_user(q) == "abhishek"

def test_extract_user_no_match():
    q = "What is the weather today?"
    assert QueryParserService.extract_user(q) is None
