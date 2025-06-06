import datetime
from json import dumps

def datetime_serializer(obj):
    if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
        return obj.isoformat()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def serialize_dicts(dicts):
    return dumps(dicts, default=datetime_serializer)
