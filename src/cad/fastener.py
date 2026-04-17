from build123d import *


class SlidingTNut(BasePartObject):
    def __init__(
        self,
        hole_radius: float,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] | None = None,
        mode: Mode = Mode.ADD,
    ):
        with BuildPart() as main:
            with BuildSketch(Plane.YZ):
                with BuildLine():
                    Polyline(
                        (0, 4.5),
                        (3.1, 4.5),
                        (3.1, 3),
                        (4.75, 3),
                        (4.75, 2),
                        (2.75, 0),
                        (0, 0),
                    )
                    mirror(about=Plane.YZ)
                make_face()
            extrude(amount=4.75, both=True)
            Hole(hole_radius)

        super().__init__(main.part, rotation=rotation, align=align, mode=mode)
