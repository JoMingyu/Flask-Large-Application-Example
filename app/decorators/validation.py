from enum import Enum
from functools import wraps
from typing import Type

from flask import request
from pydantic import BaseModel, ValidationError

from app.context import context_property


class PayloadLocation(Enum):
    ARGS = "args"
    JSON = "json"


def validate_with_pydantic(
    *,
    payload_location: PayloadLocation,
    model: Type[BaseModel],
    json_force_load: bool = False,
):
    """
    Decorator to validate a json payload.

    Args:
        payload_location: (todo): write your description
        model: (todo): write your description
        json_force_load: (bool): write your description
    """
    def decorator(fn):
        """
        Decorator to add a decorators.

        Args:
            fn: (str): write your description
        """
        @wraps(fn)
        def wrapper(*args, **kwargs):
            """
            Decorator to wrap_json.

            Args:
            """
            if payload_location == PayloadLocation.JSON:
                if json_force_load:
                    payload = request.get_json(force=True)
                else:
                    payload = request.json
            else:
                payload = request.args

                if hasattr(payload, "to_dict"):
                    payload = payload.to_dict()

            try:
                instance = model(**payload)
            except ValidationError:
                raise
            except:
                instance = None

            context_property.request_payload = instance

            return fn(*args, **kwargs)

        return wrapper

    return decorator
