from typing import List, Optional

from data_class.field import Field
from data_class.model.base import BaseModel


class IDInput(BaseModel):
    id: int


class Fault(BaseModel):
    title: str
    directory_id: IDInput = Field(alias="directory")
    reasons: Optional[List[IDInput]]


class UpdateFault(BaseModel):
    title: Optional[str]
    c: List[Fault]


class User(BaseModel):
    name: Optional[str]
    age: Optional[int]


class Dep(BaseModel):
    a: int
    b: Optional[int] = 12
    c: List[User]
    d: Optional[List[User]]


if __name__ == "__main__":
    a = Dep(a=1, c=[{"name": 1, "age": 2}, {"name": 1, "age": 2}])
    print(a.dict())
    b = UpdateFault(
        title=1, c=[{"title": 1, "directory_id": {"id": "1"}, "reasons": [{"id": 1}]}]
    )
    from pprint import pp

    pp(b.dict())
