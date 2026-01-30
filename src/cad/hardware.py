from bd_warehouse.thread import TrapezoidalThread
from build123d import *


class LeadScrew(BasePartObject):
    def __init__(
        self,
        length: float,
        simple: bool = False,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] | None = None,
        mode: Mode = Mode.ADD,
    ) -> None:
        with BuildPart() as main:
            Cylinder(
                radius=4 if simple else 3,
                height=length,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            )
            if simple:
                chamfer(main.edges(), length=1)
            else:
                chamfer(main.edges(), length=0.5)
                TrapezoidalThread(
                    diameter=8,
                    pitch=2,
                    thread_angle=30,
                    length=length,
                    starts=2,
                )

        super().__init__(main.part, rotation=rotation, align=align, mode=mode)
