from typing import Any, Callable

from pyruicore.data_type import BaseType


class Field:
    __slots__ = (
        "field_type",
        "mock_func",
        "enum_values",
        "comment",
        "nullable",
        "validate",
        "implicit",
        "default",
        "default_factory",
    )

    def __init__(
        self,
        field_type: BaseType = None,
        mock_func: Callable = None,
        enum_values: tuple = (),
        comment: str = "",
        nullable: bool = True,
        validate: Callable = None,
        implicit: bool = True,
        default: Any = None,
        default_factory: Callable = None,
        **kwargs,
    ):
        self.field_type = field_type
        self.mock_func = mock_func
        self.enum_values = enum_values
        self.comment = comment
        self.nullable = nullable
        self.validate = validate
        self.implicit = implicit
        self.default = default
        self.default_factory = default_factory

    def get_value(self, value):
        if value is None:
            if self.default_factory is not None:
                value = self.default_factory()
            elif self.default is not None:
                value = self.default
            else:
                return None
        return value

    def parse(self, field, value):
        if not self.implicit:
            self.field_type.validate(value)
        return self.field_type.parse(field, value)

    def __str__(self):
        return f"<Field of type : {self.field_type or 'unknown yet'}>"

    __repr__ = __str__
