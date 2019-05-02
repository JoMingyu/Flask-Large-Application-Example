from enum import Enum
from functools import wraps
from typing import Type

from flask import request
from pydantic import BaseModel

from app.context import context_property


class PayloadLocation(Enum):
    ARGS = 'args'
    JSON = 'json'


def validate_with_pydantic(payload_location: PayloadLocation, model: Type[BaseModel]):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            payload = getattr(request, payload_location.value)

            if payload_location == PayloadLocation.ARGS:
                payload = payload.to_dict()

            instance = model(**payload)

            context_property.request_payload = instance

            return fn(*args, **kwargs)
        return wrapper
    return decorator
