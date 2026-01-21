from copy import copy

from bd_vslot.rails import VSlot2020Rail
from build123d import *
from build123d.topology.shape_core import Shape


class MainAssembly(Compound):
    def __init__(
        self,
        *,
        label: str = "",
        color: Color | None = None,
        material: str = "",
        parent: Compound | None = None,
    ):
        children: list[Shape] = []

        super().__init__(
            label=label,
            color=color,
            material=material,
            parent=parent,
            children=children,
        )
