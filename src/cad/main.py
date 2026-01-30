from build123d import *
from build123d.topology.shape_core import Shape

from cad.bed import BedAssembly
from cad.frame import FrameAssembly
from cad.x_axis import XAxisAssembly


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

        frame = FrameAssembly(label="frame")
        children.append(frame)

        x_axis = XAxisAssembly(label="x-axis").move(Location((0, -150, 0), (0, 0, 0)))
        children.append(x_axis)

        bed = BedAssembly(label="bed").move(Location((0, -200, 46), (0, 0, 0)))
        children.append(bed)

        super().__init__(
            label=label,
            color=color,
            material=material,
            parent=parent,
            children=children,
        )
