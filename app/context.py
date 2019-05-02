from typing import Optional, Type

from flask import current_app, request, g
from pydantic import BaseModel


class _ContextProperty:
    class Key:
        request_payload = 'request_payload'

    @property
    def secret_key(self) -> str:
        return current_app.secret_key

    @property
    def user_agent(self) -> str:
        return request.headers['user_agent']

    @property
    def remote_addr(self) -> str:
        return request.remote_addr

    # - request payload -

    @property
    def request_payload(self) -> Optional[BaseModel]:
        return getattr(g, self.Key.request_payload, None)

    @request_payload.setter
    def request_payload(self, value: Type[BaseModel]):
        setattr(g, self.Key.request_payload, value)


context_property = _ContextProperty()
