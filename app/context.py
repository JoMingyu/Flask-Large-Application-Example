from typing import Optional, Type

from flask import current_app, g
from pydantic import BaseModel


class _ContextLocalData:
    def __init__(self, key_name, default):
        """
        Initialize a new key.

        Args:
            self: (todo): write your description
            key_name: (str): write your description
            default: (str): write your description
        """
        self.key_name = key_name
        self.default = default

    def get(self, _g):
        """
        Returns the value of a key.

        Args:
            self: (todo): write your description
            _g: (int): write your description
        """
        return getattr(_g, self.key_name, self.default)

    def set(self, _g, value):
        """
        Set the given key on the given key.

        Args:
            self: (todo): write your description
            _g: (dict): write your description
            value: (todo): write your description
        """
        setattr(_g, self.key_name, value)


class _ContextProperty:
    class ContextLocalData:
        request_payload = _ContextLocalData("request_payload", None)

    @property
    def secret_key(self) -> str:
        """
        Returns the secret key.

        Args:
            self: (todo): write your description
        """
        return current_app.secret_key

    # - request payload -

    @property
    def request_payload(self) -> Optional[BaseModel]:
        """
        The request payload.

        Args:
            self: (todo): write your description
        """
        return self.ContextLocalData.request_payload.get(g)

    @request_payload.setter
    def request_payload(self, value: Type[BaseModel]):
        """
        The payload payload.

        Args:
            self: (todo): write your description
            value: (str): write your description
        """
        self.ContextLocalData.request_payload.set(g, value)


context_property = _ContextProperty()
