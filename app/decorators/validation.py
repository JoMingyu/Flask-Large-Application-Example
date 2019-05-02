from enum import Enum
from functools import wraps
from typing import Type

from flask import abort, request
from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError

from app.context import context_property


class PayloadLocation(Enum):
    ARGS = 'args'
    JSON = 'json'


def validate_with_pydantic(payload_location: PayloadLocation, model: Type[BaseModel]):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                instance = model(**getattr(request, payload_location.value))

                context_property.request_payload = instance
                return fn(*args, **kwargs)
            except ValidationError as e:
                abort(400, e.json())
        return wrapper
    return decorator
