from typing import Any, Dict, Union

from pyruicore.data_type import BaseType


class UserDefineType(BaseType):
    def __init__(self, class_: Any):
        self.class_name = class_.__name__
        self.class_type = class_

    def mock(self):
        raise NotImplementedError()

    def parse(self, field, value: Union[Dict[str, Any]]) -> Any:
        from pyruicore.model.base import BaseModel

        if isinstance(value, BaseModel):
            return value
        elif isinstance(value, dict):
            return self.class_type(**value)
        else:
            raise TypeError(
                f"<{field}> expect: <class '{self.class_name}'>, but get: {type(value)}"
            ) from None
            # todo: raise exception ?

    def validate(self, value: Any) -> None:
        assert isinstance(
            value, self.class_type
        ), f"Expect: {self.class_name} - Actual: {type(value)}"
        self.parse(value)

    def marshal(self, value) -> Any:
        return value.dict()

    @property
    def name(self):
        return self.class_name

    def __str__(self):
        return self.class_name

    __name__ = name
