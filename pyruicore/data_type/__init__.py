"""
all basic type
"""
from datetime import datetime

from pyruicore.data_type.analysis import analysis_annotation
from pyruicore.data_type.basic import (
    AnyType,
    BaseType,
    BooleanType,
    DateTimeType,
    FloatType,
    IntType,
    ListType,
    StringType,
)
from pyruicore.data_type.udf import UserDefineType

TYPE_MAPPING = {
    int: IntType,
    str: StringType,
    float: FloatType,
    list: ListType,
    datetime: DateTimeType,
}

__all__ = [
    "BaseType",
    "IntType",
    "FloatType",
    "StringType",
    "BooleanType",
    "DateTimeType",
    "ListType",
    "TYPE_MAPPING",
    "UserDefineType",
    "AnyType",
    "analysis_annotation",
]
