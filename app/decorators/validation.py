from functools import wraps
from typing import Type, Optional

from flask import request
from pydantic import BaseModel, ValidationError

from app.context import context_property


def _validate(payload: Optional[dict], model: Type[BaseModel]) -> Optional[BaseModel]:
    if payload is None:
        payload = {}

    try:
        instance = model(**payload)
    except ValidationError:
        raise
    except:
        instance = None

    return instance


def validate(
    *,
    path_params: Type[BaseModel] = None,
    query_params: Type[BaseModel] = None,
    json: Type[BaseModel] = None,
    json_force_load: bool = False,
):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if path_params:
                payload = kwargs
                instance = _validate(payload, path_params)
                context_property.request_path_params = instance

            if query_params:
                payload = request.args
                instance = _validate(payload, query_params)
                context_property.request_query_params = instance

            if json:
                if json_force_load:
                    payload = request.get_json(force=True)
                else:
                    payload = request.json

                if hasattr(payload, "to_dict"):
                    payload = payload.to_dict()

                instance = _validate(payload, json)
                context_property.request_json = instance

            return fn(*args, **kwargs)

        return wrapper

    return decorator
