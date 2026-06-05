from dataclasses import asdict, is_dataclass


def serialize(obj):

    if is_dataclass(obj):
        return asdict(obj)

    if isinstance(obj, list):
        return [serialize(x) for x in obj]

    if hasattr(obj, "__dict__"):
        return vars(obj)

    return obj