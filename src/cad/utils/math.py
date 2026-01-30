from math import cos, radians, sin
from typing import Iterator


def polar_to_cartesian(
    radius: float,
    angle: float,
    *,
    degrees: bool = False,
) -> tuple[float, float]:
    if not degrees:
        angle = radians(angle)
    x = radius * cos(angle)
    y = radius * sin(angle)
    return x, y


def float_range(
    start: float,
    stop: float,
    step: float = 1.0,
) -> Iterator[float]:
    current = start
    while current < stop:
        yield current
        current += step
