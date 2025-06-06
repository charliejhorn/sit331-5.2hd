import datetime
from json import dumps

def datetime_serializer(obj):
    print("datetime_serializer: " + str(obj))
    if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
        return obj.isoformat()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable, by the way this was us")

def serialize_dicts(dicts):
    return dumps(dicts, default=datetime_serializer)

def datetime_deserializer(obj):
    if isinstance(obj, str):
        try:
            return datetime.datetime.fromisoformat(obj)
        except ValueError:
            pass
    return obj