from datetime import datetime

from pyruicore.data_type.const import DATE_FORMATS


def str_to_datetime(value):
    ret = None
    if value and value not in {"", "null", "None"}:
        for format_ in DATE_FORMATS:
            try:
                ret = datetime.strptime(value, format_)
            except ValueError:
                pass
            else:
                break
        else:
            raise Exception(
                f"[date] [time] [datetime] format must be {DATE_FORMATS}, Actual: [{value}]"
            ) from None
    return ret
