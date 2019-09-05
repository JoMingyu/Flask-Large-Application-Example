from pydantic import conint
from pydantic.dataclasses import dataclass


@dataclass
class Post:
    age: conint(gt=0)
    name: str
