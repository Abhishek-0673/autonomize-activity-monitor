def success(message: str, items=None, meta: dict = None):
    """Success response builder."""
    return {
        "success": True,
        "message": message,
        "data": {
            "items": items if items is not None else [],
            "meta": meta if meta is not None else {}
        }
    }


def failure(message: str, error: str = None):
    """Failure response builder."""
    return {
        "success": False,
        "message": message,
        "error": error
    }
