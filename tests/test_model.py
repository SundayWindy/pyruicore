from datetime import datetime
from typing import Any, List, Optional, Text

from pyruicore import BaseModel, Field


def test_single_type():
    class User(BaseModel):
        age: int
        name: str
        address: Text
        birth: datetime

    user = User(age=1, name="12", address="address", birth="2020-09-09 11:11:11")
    expect = {
        "age": 1,
        "name": "12",
        "address": "address",
        "birth": "2020-09-09 11:11:11",
    }
    assert user.dict() == expect


def test_list_single_type():
    class User(BaseModel):
        age: int
        names: List[str]
        awards: List[int]

    user = User(age="1", names=["name1", "name2"], awards=[1, 2, 3])
    expect = {"age": 1, "names": ["name1", "name2"], "awards": [1, 2, 3]}
    assert user.dict() == expect


def test_model_type():
    class Department(BaseModel):
        name: str
        address: str

    class User(BaseModel):
        age: int
        departs: Department

    user = User(age=1, departs={"name": "de1", "address": "address1"})
    expect = {"age": 1, "departs": {"name": "de1", "address": "address1"}}
    assert user.dict() == expect


def test_list_model_type():
    class Department(BaseModel):
        name: str
        address: str

    class User(BaseModel):
        age: int
        departs: List[Department]

    user = User(
        age=1,
        departs=[
            {"name": "de1", "address": "address1"},
            Department(name="2", address="address2"),
        ],
    )
    expect = {
        "age": 1,
        "departs": [
            {"name": "de1", "address": "address1"},
            {"name": "2", "address": "address2"},
        ],
    }
    assert user.dict() == expect


def test_optional():
    class User(BaseModel):
        age: int
        name: str
        email: Optional[str]

    user = User(age=1, name="name1")
    expect = {"age": 1, "name": "name1", "email": None}
    assert user.dict() == expect


def test_default():
    class User(BaseModel):
        age: int = Field(default=1)
        name: str

    user = User(name="name")
    expect = {"age": 1, "name": "name"}
    assert user.dict() == expect


def test_default_factory():
    class User(BaseModel):
        age: int = Field(default_factory=lambda: 1)
        name: str

    user = User(name="name")
    expect = {"age": 1, "name": "name"}
    assert user.dict() == expect


def test_any_type():
    class Dept(BaseModel):
        name: str = Field(default_factory=lambda: "dept")

    class User(BaseModel):
        age: int = Field(default_factory=lambda: 1)
        dept: Any = Field(default_factory=lambda: Dept())

    user = User()
    expect = {"age": 1, "dept": {"name": "dept"}}
    assert user.dict() == expect
