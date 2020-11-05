from flask import Response


def after_request(response: Response) -> Response:
    """
    Handles the headers.

    Args:
        response: (todo): write your description
    """
    try:
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "deny"
    finally:
        return response
