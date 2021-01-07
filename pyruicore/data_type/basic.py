from collections.abc import Iterable
from datetime import datetime
from random import choice, randint, random
from typing import Any, List, Optional, Union

from pyruicore.data_type.util import str_to_datetime


class BaseType:
    def mock(self) -> Any:
        raise NotImplementedError()

    def parse(self, field, value) -> Any:
        raise NotImplementedError()

    def validate(self, value) -> Any:
        raise NotImplementedError()

    def marshal(self, value) -> Any:
        raise NotImplementedError()

    def __str__(self) -> str:
        return self.__class__.__name__

    __repr__ = __str__
    __name__ = "base_type"


class IntType(BaseType):
    def mock(self) -> int:
        return randint(0, 10)

    def parse(self, field, value) -> Optional[int]:
        try:
            return int(value) if value not in (None, "") else None
        except TypeError:
            raise TypeError(f"{field} expect <class 'int'>, but get {type(value)}")

    def marshal(self, value) -> Optional[int]:
        return int(value) if value is not None else None

    def validate(self, value) -> None:
        assert value is None or isinstance(
            value, int
        ), f"expect <class 'int'>, but get {type(value)}"

    __name__ = "int"


class FloatType(BaseType):
    def mock(self) -> float:
        return int(random() * 100) / 10

    def parse(self, field, value) -> float:
        try:
            return float(value) if value not in (None, "") else None
        except TypeError:
            raise TypeError(f"{field} expect <class 'float'>, but get {type(value)}")

    def marshal(self, value) -> Optional[float]:
        return float(value) if value is not None else None

    def validate(self, value) -> None:
        assert value is None or isinstance(
            value, float
        ), f"expect <class 'float'>, but get {type(value)}"

    __name__ = "float"


class StringType(BaseType):
    def mock(self) -> str:
        return str(random() * 100 / 10)

    def parse(self, field, value) -> Optional[str]:
        try:
            return str(value) if value not in (None, "") else None
        except TypeError:
            raise TypeError(f"{field} expect <class 'str'>, but get {type(value)}")

    def marshal(self, value) -> Optional[str]:
        return str(value) if value is not None else None

    def validate(self, value) -> None:
        assert value is None or isinstance(
            value, str
        ), f"expect <class 'str'>, but get {type(value)}"

    __name__ = "str"


class BooleanType(BaseType):
    def mock(self) -> bool:
        return choice([True, False])

    def parse(self, field, value) -> bool:
        return True if value else False

    def validate(self, value) -> None:
        assert value is None or isinstance(
            value, bool
        ), f"expect <class 'bool'>, but get {type(value)}"

    def marshal(self, value):
        return True if value else False

    __name__ = "bool"


class DateTimeType(BaseType):
    def mock(self) -> datetime:
        return datetime.fromtimestamp(1000000000 * random())

    def parse(self, field, value) -> datetime:
        if value and value not in {"", "null", "None"}:
            if isinstance(value, datetime):
                return value
            elif isinstance(value, str):
                return str_to_datetime(value)

        raise ValueError(f"{field} expect datetime, but get{value},Invalid datetime type")

    def marshal(self, value):
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return None

    def validate(self, value) -> None:
        assert value is None or isinstance(
            value, datetime
        ), f"expect <class 'datetime'>, but get {type(value)}"

    __name__ = "datetime"


class ListType(BaseType):
    """ list 目前仅支持单一类型"""

    def __init__(self, element_type: Union[BaseType, Any]) -> None:
        self.element_type = element_type

    def mock(self) -> List[Any]:
        return [self.element_type.mock() for _ in range(10)]

    def parse(self, field, value) -> List[Any]:
        try:
            return [] if not value else [self.element_type.parse(field, v) for v in value]
        except TypeError as e:
            raise e

    def validate(self, value) -> None:
        assert isinstance(value, Iterable) and not isinstance(
            value, str
        ), f"expect <Iterable> and not <class 'str'>, but get {type(value)}"
        [self.element_type.validate(v) for v in value]  # 基本类型

    def marshal(self, value) -> List[Any]:
        return [self.element_type.marshal(v) for v in value]

    def __str__(self):
        return f"List of <{self.element_type.__name__}>"

    __name__ = "list"
