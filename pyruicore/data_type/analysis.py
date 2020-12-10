from typing import Any, Callable, Tuple, Union, get_args, get_origin

NoneType = type(None)


def is_origin_type(type_hint):
    return isinstance(type_hint, type)


def parse_union(args):
    """
    Optional[int] ==> (True, <class 'int'>,)
    Union[int,None] ==>  (True, <class 'int'>,)
    """

    nullable, types_ = False, []
    for type_ in args:
        if type_ is NoneType:
            nullable = True
        else:
            types_.append(type_)

    if len(types_) == 1:
        real_type = types_[0]
        if get_args(real_type):
            _, real_type, ele_type = analysis_annotation(real_type)
            return nullable, real_type, ele_type
        else:
            return nullable, real_type, None

    raise Exception(f"不支持嵌套类型{args}")


def check_args(args, error=""):
    if len(args) > 2:
        raise Exception(f"不支持嵌套类型{args}")
    if len(args) == 2 and NoneType not in args:
        raise Exception(f"不支持嵌套类型{args}")
    assert all(is_origin_type(arg) for arg in args), f"{error}: {args}"


def analysis_annotation(type_hint: Any) -> Tuple[bool, Any, Any]:
    """
    根据 typing 获取真实的类型
    返回是否可空，以及真实的类型
    """
    if is_origin_type(type_hint) and not get_args(type_hint):
        return False, type_hint, None  # 原始单一类型

    if type_hint is Callable:  # func
        raise Exception(f"不支持 {Callable} 类型") from None

    origin, args = get_origin(type_hint), get_args(type_hint)

    if is_origin_type(origin):
        check_args(args, error=f"类型 {origin} 下不支持")
        return False, origin, args[0]
    if origin is Union:
        return parse_union(args)

    raise Exception(f"不支持 {type_hint} 类型") from None
