from os import getenv


def getbool(key: str, default: bool = False) -> bool:
    value = getenv(key)
    if value is None:
        return default
    if value.lower() in ("1", "true", "yes", "on"):
        return True
    if value.lower() in ("0", "false", "no", "off"):
        return False
    return default


def getfloat(key: str, default: float = 0.0) -> float:
    value = getenv(key)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


SIMPLE = getbool("SIMPLE", True)

X = getfloat("X")
Y = getfloat("Y")
Z = getfloat("Z")
