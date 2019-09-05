from enum import Enum
from functools import wraps

from dacite import from_dict, Config
from flask import request

from app.context import context_property


class PayloadLocation(Enum):
    ARGS = "args"
    JSON = "json"


def validate_with_pydantic(payload_location: PayloadLocation, model):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            payload = getattr(request, payload_location.value)

            if payload_location == PayloadLocation.ARGS and hasattr(payload, "to_dict"):
                payload = payload.to_dict()

            instance = from_dict(data_class=model, data=payload, config=Config(check_types=False))

            context_property.request_payload = instance

            return fn(*args, **kwargs)

        return wrapper

    return decorator
