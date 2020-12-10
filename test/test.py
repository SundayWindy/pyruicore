from typing import List, Optional
from uuid import uuid4

from pyruicore.field import Field
from pyruicore.model.base import BaseModel


class IDInput(BaseModel):
    id: int = Field(default=1, default_factory=lambda: 3)


class Fault(BaseModel):
    title: str = "122"
    directory_id: IDInput = Field(alias="directory")
    reasons: Optional[List[IDInput]]


class UpdateFault(BaseModel):
    title: Optional[str]
    c: List[Fault]
    d: Optional[int] = Field(default_factory=uuid4)


class User(BaseModel):
    name: Optional[str]
    age: Optional[int]
    d: int = Field(default_factory=uuid4)


class Dep(BaseModel):
    a: int
    b: Optional[int] = 1000
    c: List[User]
    d: Optional[List[User]]


if __name__ == "__main__":
    b = UpdateFault(
        title=1, c=[{"title": 1, "directory_id": {"id": "1"}, "reasons": [{"id": 1}]}]
    )

    from pprint import pprint

    pprint(b.dict())
    print(int(uuid4()))
