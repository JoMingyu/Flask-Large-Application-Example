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
        request_path_params = _ContextLocalData("request_path_params", None)
        request_query_params = _ContextLocalData("request_query_params", None)
        request_json = _ContextLocalData("request_json", None)

    @property
    def secret_key(self) -> str:
        return current_app.secret_key

    # - request payload -

    @property
    def request_path_params(self) -> Optional[BaseModel]:
        return self.ContextLocalData.request_path_params.get(g)

    @request_path_params.setter
    def request_path_params(self, value: Type[BaseModel]):
        self.ContextLocalData.request_path_params.set(g, value)

    @property
    def request_query_params(self) -> Optional[BaseModel]:
        return self.ContextLocalData.request_query_params.get(g)

    @request_query_params.setter
    def request_query_params(self, value: Type[BaseModel]):
        self.ContextLocalData.request_query_params.set(g, value)

    @property
    def request_json(self) -> Optional[BaseModel]:
        return self.ContextLocalData.request_json.get(g)

    @request_json.setter
    def request_json(self, value: Type[BaseModel]):
        self.ContextLocalData.request_json.set(g, value)


context_property = _ContextProperty()
