from typing import Optional, Type

from flask import current_app, g
from pydantic import BaseModel


class _ContextLocalData:
    def __init__(self, key_name, default):
        self.key_name = key_name
        self.default = default

    def get(self, _g):
        return getattr(_g, self.key_name, self.default)

    def set(self, _g, value):
        setattr(_g, self.key_name, value)


class _ContextProperty:
    class ContextLocalData:
        request_payload = _ContextLocalData("request_payload", None)

    @property
    def secret_key(self) -> str:
        return current_app.secret_key

    # - request payload -

    @property
    def request_payload(self) -> Optional[BaseModel]:
        return self.ContextLocalData.request_payload.get(g)

    @request_payload.setter
    def request_payload(self, value: Type[BaseModel]):
        self.ContextLocalData.request_payload.set(g, value)


context_property = _ContextProperty()
