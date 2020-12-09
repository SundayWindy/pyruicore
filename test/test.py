from typing import List, Optional

from data_class.model.base import BaseModel


class A(BaseModel):
    a: int
    b: str
    parse: Optional[int]


class T(BaseModel):
    a: int
    b: Optional[int] = 12
    c: List[A]
    d: Optional[List[A]]

    __name__: int = None


if __name__ == "__main__":
    a = T(a=1, c=[{"a": 1, "b": 2}, {"a": 1, "b": 2}])
    print(a.dict())
