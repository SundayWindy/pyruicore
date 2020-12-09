from datetime import datetime

from data_type.analysis import analysis_annotation
from data_type.basic import (
    BaseType,
    BooleanType,
    DateTimeType,
    FloatType,
    IntType,
    ListType,
    StringType,
)
from data_type.udf import UserDefineType

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
    "analysis_annotation",
]
