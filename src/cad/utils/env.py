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


SIMPLE = getbool("SIMPLE")
