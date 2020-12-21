from pydantic import conint, BaseModel


class PostJson(BaseModel):
    age: conint(gt=0)
    name: str


class PostResponse(BaseModel):
    msg: str
