from typing import Any, List

from pyruicore.data_type import TYPE_MAPPING, ListType, UserDefineType, analysis_annotation
from pyruicore.field import Field


class ModelMetaClass(type):
    def __new__(mcs, cls_name: str, bases: tuple, attrs: dict):
        __fields_map__: [str, Field] = {}

        copy_bases(__fields_map__, bases)
        init_annotations(__fields_map__, attrs)

        attrs["__fields__"] = tuple(__fields_map__.values())
        attrs["__fields_map__"] = __fields_map__
        attrs["__slots__"] = (
            tuple(attrs.get("__slots__", ())) + tuple(__fields_map__.keys()) + ("__storage__",)
        )

        return type.__new__(mcs, cls_name, bases, attrs)


def copy_bases(__fields_map__, bases):
    """copy all field in base class to current class, ignore repeat field, in-place"""
    for base in bases:
        for field in getattr(base, "__fields__", ()):
            if field.name not in __fields_map__:
                __fields_map__[field.name] = field


def init_annotations(__fields_map__, attrs):
    """init Field from user given annotations, in-place"""
    for field_name, anno_type in attrs.get("__annotations__", {}).items():
        if is_reserve_word(field_name):
            continue
        user_ini_field = attrs.pop(field_name, None)  # user init Field
        __fields_map__[field_name] = init_field(user_ini_field, anno_type, field_name)


def init_field(user_ini_field: Field, anno_type: [int, str, float, List, Any], field_name: str):
    nullable, user_field_type, user_ele_type = parse_annotation(anno_type)
    field_type = init_field_type(user_field_type, user_ele_type)

    field = parse_ugv_field(user_ini_field) or Field()
    field.nullable, field.field_type, field.name = nullable, field_type, field_name
    return field


def is_reserve_word(word: str):
    """word start with `_` is treated as a reserve word"""
    return word.startswith("_")


def is_model_type(field_type: Any):
    """ check if field_type is user define model """
    return isinstance(field_type, ModelMetaClass)


def init_field_type(user_field_type, user_ele_type):
    """ init `field_type` for `Field`"""
    if is_model_type(user_field_type):
        return init_model_type(user_field_type)

    field_type = TYPE_MAPPING.get(user_field_type)
    if field_type is None:
        raise Exception(f"暂时不支持 {user_field_type} 类型")

    if field_type is ListType:
        return init_list_type(user_ele_type)

    return field_type()  # basic type <IntType,StringType ... > we can just init it


def parse_ugv_field(user_ini_field):
    """
    parse user given Field:
    if user_ini_field is type <BaseType>, do nothing, return it;
    else treat user_ini_field as a default value
    """
    if not isinstance(user_ini_field, Field):
        user_ini_field = Field(default=user_ini_field)
    return user_ini_field


def init_model_type(class_type: Any) -> Any:
    """init field_type of type <UserDefineType>"""
    return UserDefineType(class_=class_type)


def init_list_type(field_ele_type):
    """ init field_type of <ListType> """
    if isinstance(field_ele_type, ModelMetaClass):
        return ListType(element_type=UserDefineType(class_=field_ele_type))

    ele_type = TYPE_MAPPING.get(field_ele_type)
    if ele_type is None:
        raise Exception(f"暂时不支持 {field_ele_type} 类型")
    return ListType(element_type=ele_type())


def parse_annotation(field_type):
    """ get `nullable`, `type`, `ele_type(if is List)` from annotation"""
    try:
        nullable, user_field_type, user_ele_type = analysis_annotation(field_type)
    except Exception as e:
        raise e

    return nullable, user_field_type, user_ele_type
