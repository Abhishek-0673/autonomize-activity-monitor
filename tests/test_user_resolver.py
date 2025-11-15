from src.core.user_resolver import UserResolver

def test_resolve_direct_name():
    assert UserResolver.resolve("abhishek") is not None

def test_resolve_case_insensitivity():
    assert UserResolver.resolve("ABHISHEK") is not None

def test_resolve_full_name():
    assert UserResolver.resolve("Abhishek S") is not None

def test_resolve_unknown_user():
    assert UserResolver.resolve("RandomGuy") is None
