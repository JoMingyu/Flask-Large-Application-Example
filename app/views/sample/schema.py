from pydantic import conint, BaseModel


class Post(BaseModel):
    age: conint(gt=0)
    name: str
