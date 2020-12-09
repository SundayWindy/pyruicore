import pprint
from typing import Any

from data_class.model.meta import ModelMetaClass


class BaseModel(metaclass=ModelMetaClass):
    __fields__ = ()
    __fields_map__ = {}

    def __init__(self, drop_missing=False, **kwargs):
        for field_name, field in self.__fields_map__.items():
            value = kwargs.get(field_name)
            if not drop_missing and not field.nullable and not value:
                raise Exception(
                    f"{type(self)}: field <{field_name}> must be initialized"
                )
            setattr(self, field_name, field.parse(value))

    def dict(self, exclude_none=False, exclude_unset=False, exclude=None):
        dct = {}
        for field_name, field in self.__fields_map__.items():
            value = self.get(field_name)
            dct[field_name] = field.field_type.marshal(value)

        return dct

    def get(self, key, default=None) -> Any:
        return getattr(self, key, default)

    def __str__(self):
        return f"<{self.__class__.__name__}>: \n{pprint.pformat(self.dict(), indent=4)}"

    def __repr__(self):
        return self.__class__.__name__
