from pydantic import BaseModel, conint


class Post(BaseModel):
    age: conint(gt=0)
    name: str
