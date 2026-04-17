from typing import Literal

from build123d import *


class EG15LinearRail(BasePartObject):
    def __init__(
        self,
        length: float,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] | None = None,
        mode: Mode = Mode.ADD,
    ) -> None:
        with BuildPart() as main:
            with BuildSketch():
                with BuildLine():
                    Polyline(
                        (0, 0),
                        (7.5, 0),
                        (7.5, 2.5),
                        (5.5, 4.5),
                        (5.5, 7.5),
                        (7.5, 7.5),
                        (7.5, 12.5),
                        (0, 12.5),
                    )
                    mirror(about=Plane.YZ)
                make_face()
                with Locations((0, 10)):
                    with GridLocations(
                        x_spacing=15,
                        y_spacing=5,
                        x_count=2,
                        y_count=2,
                    ):
                        Circle(1.25, mode=Mode.SUBTRACT)
            extrude(amount=length)
            chamfer(main.edges().filter_by(Plane.XY), length=1.0)
            with BuildSketch(Plane.XZ):
                with Locations((0, length / 2)):
                    with GridLocations(
                        x_spacing=0,
                        y_spacing=60,
                        x_count=1,
                        y_count=(length - 20) // 60 + 1,
                    ):
                        Circle(3.75)
            extrude(until=Until.FIRST, mode=Mode.SUBTRACT)
            chamfer(main.edges(Select.LAST).group_by(Axis.Y)[-1], length=0.5)

        super().__init__(main.part, rotation=rotation, align=align, mode=mode)


class EG15LinearBearing(BasePartObject):
    def __init__(
        self,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] | None = None,
        mode: Mode = Mode.ADD,
    ):
        with BuildSketch() as hole:
            with BuildLine():
                Polyline(
                    (0.0, 0.0),
                    (5.75, 0.0),
                    (5.75, 3.0),
                    (7.75, 5.0),
                    (7.75, 6.5),
                    (5.75, 8.5),
                    (0.0, 8.5),
                )
                mirror(about=Plane.YZ)
            make_face()

        with BuildSketch() as profile:
            Rectangle(33.5, 19, align=(Align.CENTER, Align.MIN))
            chamfer(profile.vertices(), length=1.0)
            add(hole.sketch, mode=Mode.SUBTRACT)

        with BuildPart() as blocks:
            with Locations((-11, 15.75, 0), (+11, 15.75, 0)):
                Box(12, 7, 40)
            chamfer(blocks.edges().filter_by(Axis.Z), length=1.0)

        with BuildPart() as main:
            with BuildSketch():
                add(profile)
            extrude(amount=26.5, both=True)
            with BuildSketch(Plane.XY.move(Location((0, 0, 26.5)))):
                add(profile)
            extrude(amount=2.0, taper=10)
            with BuildSketch(Plane.XY.move(Location((0, 0, -26.5)))):
                add(profile)
            extrude(amount=-2.0, taper=10)
            add(blocks.part)
            with BuildSketch(Plane.XZ.move(Location((0, 10, 0)))):
                with GridLocations(
                    x_spacing=26,
                    y_spacing=26,
                    x_count=2,
                    y_count=2,
                ):
                    Circle(1.75)
            extrude(until=Until.FIRST, mode=Mode.SUBTRACT)
            chamfer(main.edges(Select.LAST).group_by(Axis.Y)[-1], length=0.5)

        super().__init__(main.part, rotation=rotation, align=align, mode=mode)


class MGN15LinearRail(BasePartObject):
    def __init__(
        self,
        length: float,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] | None = None,
        mode: Mode = Mode.ADD,
    ) -> None:
        with BuildPart() as main:
            with BuildSketch():
                Rectangle(15, 10)
                with Locations((+7.5, 1.75), (-7.5, 1.75)):
                    Circle(1.25, mode=Mode.SUBTRACT)
            extrude(amount=length)
            chamfer(main.edges().filter_by(Plane.XY), length=1.0)
            with BuildSketch(Plane.XZ):
                with Locations((0, length / 2)):
                    with GridLocations(
                        x_spacing=0,
                        y_spacing=40,
                        x_count=1,
                        y_count=(length - 20) // 40 + 1,
                    ):
                        Circle(1.75)
            extrude(until=Until.LAST, mode=Mode.SUBTRACT)
            with BuildSketch(Plane.XZ):
                with Locations((0, length / 2)):
                    with GridLocations(
                        x_spacing=0,
                        y_spacing=40,
                        x_count=1,
                        y_count=(length - 20) // 40 + 1,
                    ):
                        Circle(3)
            extrude(until=Until.FIRST, mode=Mode.SUBTRACT)
            chamfer(main.edges(Select.LAST).group_by(Axis.Y)[-1], length=0.5)

        super().__init__(main.part, rotation=rotation, align=align, mode=mode)


class MGN15LinearBearing(BasePartObject):
    def __init__(
        self,
        variant: Literal["C", "H"],
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] | None = None,
        mode: Mode = Mode.ADD,
    ):
        with BuildSketch() as profile:
            Rectangle(31.5, 11.75, align=(Align.CENTER, Align.MIN))
            chamfer(profile.vertices(), length=1.0)
            Rectangle(15.5, 6.25, align=(Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        with BuildPart() as blocks:
            with Locations((-12, 0, 0), (+12, 0, 0)):
                Box(
                    8,
                    12,
                    26.7 if variant == "C" else 43.4,
                    align=(Align.CENTER, Align.MIN, Align.CENTER),
                )
            chamfer(blocks.edges().filter_by(Axis.Z), length=1.0)

        length = 42.1 if variant == "C" else 58.8

        with BuildPart() as main:
            with BuildSketch():
                add(profile)
            extrude(amount=length / 2 - 2, both=True)
            with BuildSketch(Plane.XY.move(Location((0, 0, length / 2 - 2)))):
                add(profile)
            extrude(amount=2.0, taper=10)
            with BuildSketch(Plane.XY.move(Location((0, 0, 2 - length / 2)))):
                add(profile)
            extrude(amount=-2.0, taper=10)
            add(blocks.part)
            with BuildSketch(Plane.XZ.move(Location((0, 12, 0)))):
                with GridLocations(
                    x_spacing=25,
                    y_spacing=20 if variant == "C" else 25,
                    x_count=2,
                    y_count=2,
                ):
                    Circle(1.5)
            extrude(until=Until.LAST, mode=Mode.SUBTRACT)
            chamfer(main.edges(Select.LAST).group_by(Axis.Y)[-1], length=0.5)

        super().__init__(main.part, rotation=rotation, align=align, mode=mode)
