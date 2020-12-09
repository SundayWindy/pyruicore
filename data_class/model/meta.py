from typing import Any, List, Set

from data_class.field import Field
from data_type import TYPE_MAPPING, ListType, UserDefineType, analysis_annotation


class ModelMetaClass(type):
    def __new__(mcs, cls_name: str, bases: tuple, attrs: dict):
        __fields_map__ = {}

        for base in bases:
            for field in getattr(base, "__fields__", ()):
                if field.name not in __fields_map__:
                    __fields_map__[field.name] = field

        for field_name, field_type in attrs.get("__annotations__", {}).items():
            if field_name.startswith("_"):
                continue
            __fields_map__[field_name] = init_field(field_type)
            attrs.pop(field_name, None)

        attrs["__fields__"] = tuple(__fields_map__.values())
        attrs["__fields_map__"] = __fields_map__
        slots: Set[str] = attrs.get("__slots__", ())
        attrs["__slots__"] = tuple(
            list(__fields_map__.keys()) + ["__storage__"] + list(slots)
        )

        return type.__new__(mcs, cls_name, bases, attrs)


def init_field(field_type: [int, str, float, List, Any]):
    nullable, udf_type, udf_ele_type = parse_annotation(field_type)

    if isinstance(udf_type, ModelMetaClass):
        return parse_udf_type(nullable, udf_type)

    field_type = TYPE_MAPPING.get(udf_type)

    if field_type is None:
        raise Exception(f"暂时不支持 {udf_type} 类型")
    if field_type is ListType:
        return parse_list_type(nullable, udf_ele_type)

    return Field(nullable=nullable, field_type=field_type())


def parse_annotation(field_type):
    try:
        nullable, udf_type, udf_ele_type = analysis_annotation(field_type)
    except Exception as e:
        raise e

    return nullable, udf_type, udf_ele_type


def parse_udf_type(nullable, udf_type):
    return Field(nullable=nullable, field_type=UserDefineType(class_=udf_type))


def parse_list_type(nullable, udf_ele_type):
    if isinstance(udf_ele_type, ModelMetaClass):
        return Field(
            nullable=nullable,
            field_type=ListType(element_type=UserDefineType(class_=udf_ele_type)),
        )
    else:
        ele_type = TYPE_MAPPING.get(udf_ele_type)
        if ele_type is None:
            raise Exception(f"暂时不支持 {udf_ele_type} 类型")
        return Field(nullable=nullable, field_type=ListType(element_type=ele_type()))
