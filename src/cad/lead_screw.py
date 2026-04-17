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


class LeadScrewJoiner(BasePartObject):
    def __init__(
        self,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] | None = None,
        mode: Mode = Mode.ADD,
    ) -> None:
        with BuildPart() as main:
            Cylinder(radius=7, height=25)
            chamfer(main.edges(), length=0.5)

        super().__init__(main.part, rotation=rotation, align=align, mode=mode)


class AntiBacklashNutBlock(BasePartObject):
    def __init__(
        self,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] | None = None,
        mode: Mode = Mode.ADD,
    ) -> None:
        with BuildPart() as main:
            with BuildSketch():
                RectangleRounded(34, 33, 3)
                with Locations((5.5, 6)):
                    SlotOverall(34, 5, mode=Mode.SUBTRACT)
                with Locations((-10, -6.5), (+10, -6.5)):
                    Circle(2.5, mode=Mode.SUBTRACT)
            extrude(amount=6, both=True)
            with BuildSketch():
                with Locations((-10, -6.5), (+10, -6.5)):
                    RegularPolygon(4, 6, major_radius=False, rotation=30)
            extrude(until=Until.LAST, mode=Mode.SUBTRACT)
            with BuildSketch(Plane.XY.move(Location((0, 0, -4)))):
                with Locations((-10, -6.5), (+10, -6.5)):
                    Circle(4.5)
            extrude(until=Until.FIRST, mode=Mode.SUBTRACT)
            chamfer(
                main.edges().group_by(Axis.Z)[0] + main.edges().group_by(Axis.Z)[-1],
                length=0.5,
            )
            with BuildSketch(Plane.XZ.move(Location((0, 16.5, 0)))):
                Circle(4)
            extrude(until=Until.LAST, mode=Mode.SUBTRACT)
            chamfer(main.edges(Select.LAST), length=0.5)
            with BuildSketch(Plane.XZ.move(Location((10, 16.5, 0)))):
                Circle(2.5)
            extrude(amount=10, mode=Mode.SUBTRACT)
            chamfer(main.edges(Select.LAST), length=1.0)

        super().__init__(main.part, rotation=rotation, align=align, mode=mode)


class BrassNut(BasePartObject):
    def __init__(
        self,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] | None = None,
        mode: Mode = Mode.ADD,
    ) -> None:
        with BuildPart() as main:
            with BuildSketch():
                Circle(11)
                with PolarLocations(radius=8, count=4):
                    Circle(1.75, mode=Mode.SUBTRACT)
            extrude(amount=3.5)
            with BuildSketch():
                Circle(5)
            extrude(amount=5)
            with BuildSketch():
                Circle(5)
            extrude(amount=-10)
            with BuildSketch():
                Circle(4)
            extrude(until=Until.LAST, both=True, mode=Mode.SUBTRACT)

        super().__init__(main.part, rotation=rotation, align=align, mode=mode)


class BrassNutSmall(BasePartObject):
    def __init__(
        self,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] | None = None,
        mode: Mode = Mode.ADD,
    ) -> None:
        with BuildPart() as main:
            with BuildSketch():
                Circle(11)
                Rectangle(25, 10.5, mode=Mode.INTERSECT)
                with PolarLocations(radius=8, count=2):
                    Circle(1.75, mode=Mode.SUBTRACT)
            extrude(amount=3.5)
            with BuildSketch():
                Circle(5)
            extrude(amount=5)
            with BuildSketch():
                Circle(4)
            extrude(until=Until.LAST, mode=Mode.SUBTRACT)

        super().__init__(main.part, rotation=rotation, align=align, mode=mode)
