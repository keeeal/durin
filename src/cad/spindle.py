from build123d import *
from build123d.topology.shape_core import Shape

from cad.lead_screw import BrassNutSmall
from cad.linear_rail import MGN15LinearBearing
from cad.utils.env import SIMPLE


class SpindleMotorBracket(BasePartObject):
    def __init__(
        self,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] | None = None,
        mode: Mode = Mode.ADD,
    ) -> None:
        with BuildPart() as main:
            with BuildSketch() as profile:
                Rectangle(50, 52, align=(Align.CENTER, Align.MIN))
                with (
                    Locations((0, 26)),
                    GridLocations(
                        x_spacing=23,
                        y_spacing=28,
                        x_count=2,
                        y_count=2,
                    ),
                ):
                    SlotOverall(10, 4, mode=Mode.SUBTRACT)
                fillet(profile.vertices().group_by(Axis.Y)[-1], radius=5)
            extrude(amount=3)
            with BuildSketch(Plane.XZ) as profile:
                Rectangle(50, 52, align=(Align.CENTER, Align.MIN))
                with Locations((0, 27)):
                    Circle(8.75, mode=Mode.SUBTRACT)
                    with GridLocations(
                        x_spacing=29,
                        y_spacing=0,
                        x_count=2,
                        y_count=1,
                    ):
                        Circle(2, mode=Mode.SUBTRACT)
                fillet(profile.vertices().group_by(Axis.Y)[-1], radius=5)
            extrude(amount=-3)

        super().__init__(main.part, rotation=rotation, align=align, mode=mode)


class FrontPlate(BasePartObject):
    def __init__(
        self,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] | None = None,
        mode: Mode = Mode.ADD,
    ) -> None:
        with BuildPart() as main:
            with BuildSketch(Plane.XZ):
                with Locations((-35, 0), (+35, 0)):
                    RectangleRounded(32, 59, radius=2)
                    with GridLocations(
                        x_spacing=25,
                        y_spacing=25,
                        x_count=2,
                        y_count=2,
                    ):
                        Circle(1.75, mode=Mode.SUBTRACT)
                with Locations((0, -19)):
                    RectangleRounded(50, 52, radius=2)
                    with GridLocations(
                        x_spacing=29,
                        y_spacing=28,
                        x_count=2,
                        y_count=2,
                    ):
                        Circle(2.25, mode=Mode.SUBTRACT)
            extrude(amount=3)

            with BuildSketch(Plane.YZ):
                with BuildLine():
                    Polyline(
                        (0, 0),
                        (10.5, 0),
                        (10.5, -3),
                        (0, -20),
                        close=True,
                    )
                make_face()
            extrude(amount=10.75, both=True)
            with BuildSketch(Plane.XY.move(Location((0, 5.25, 0)))):
                Circle(4.25)
                Rectangle(
                    width=8.5,
                    height=10,
                    align=(Align.CENTER, Align.MIN),
                )
                with GridLocations(
                    x_spacing=16,
                    y_spacing=0,
                    x_count=2,
                    y_count=1,
                ):
                    Circle(1.75)
            extrude(until=Until.FIRST, mode=Mode.SUBTRACT)
            with BuildSketch(Plane.XY.move(Location((0, 5.25, -3)))):
                with GridLocations(
                    x_spacing=16,
                    y_spacing=0,
                    x_count=2,
                    y_count=1,
                ):
                    Rectangle(width=5.6, height=10.5)
            extrude(amount=-20, mode=Mode.SUBTRACT)

        super().__init__(main.part, rotation=rotation, align=align, mode=mode)


class Motor775(BasePartObject):
    def __init__(
        self,
        *,
        simple: bool = False,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] | None = None,
        mode: Mode = Mode.ADD,
    ) -> None:
        with BuildPart() as main:
            if simple:
                with BuildSketch():
                    Circle(21)
                extrude(amount=66.5)
                fillet(main.edges().group_by(Axis.Z)[0], radius=3)
                with BuildSketch(Plane.XZ.move(Location((0, 0, 5.5), -80))):
                    with Locations((21, 0)):
                        Rectangle(1, 34, align=Align.MIN)
                revolve(revolution_arc=340)
                with BuildSketch():
                    Circle(8.75)
                extrude(amount=-4.5)
                chamfer(main.edges(Select.LAST).group_by(Axis.Z)[0], length=0.5)
                with BuildSketch():
                    Circle(7.5)
                extrude(amount=73)
                chamfer(main.edges(Select.LAST).group_by(Axis.Z)[-1], length=2.5)
                with BuildSketch() as shaft:
                    Circle(2.5)
                extrude(shaft.sketch, amount=-20.5)
                chamfer(main.edges(Select.LAST).group_by(Axis.Z)[0], length=0.5)
                extrude(shaft.sketch, amount=77.5)
                chamfer(main.edges(Select.LAST).group_by(Axis.Z)[-1], length=0.5)
            else:
                add(
                    import_step("src/cad/assets/motor-775.step").move(
                        Location((0, 0, -20.5), (0, 90, 180)),
                    ),
                )
        super().__init__(main.part, rotation=rotation, align=align, mode=mode)


class SpindleAssembly(Compound):
    def __init__(
        self,
        *,
        label: str = "",
        color: Color | None = None,
        material: str = "",
        parent: Compound | None = None,
    ) -> None:
        children: list[Shape] = []

        spindle_motor_bracket = SpindleMotorBracket().move(
            Location((0, -43, 107.5), (90, 0, 0)),
        )
        spindle_motor_bracket.label = "spindle-motor-bracket"
        children.append(spindle_motor_bracket)

        spindle_motor = Motor775(simple=SIMPLE).move(
            Location((0, -70, 110.5)),
        )
        spindle_motor.label = "spindle-motor"
        children.append(spindle_motor)

        mgn15_bearings = [
            MGN15LinearBearing(variant="H").move(
                Location((-35, -28, 152.5), 180),
            ),
            MGN15LinearBearing(variant="H").move(
                Location((+35, -28, 152.5), 180),
            ),
        ]
        for index, mgn15_bearing in enumerate(mgn15_bearings):
            mgn15_bearing.label = f"mgn15-bearing-{index}"
        children.extend(mgn15_bearings)

        brass_nut = BrassNutSmall().move(Location((0, -34.75, 152.5), (0, 0, 0)))
        brass_nut.label = "nut-block"
        children.append(brass_nut)

        front_plate = FrontPlate().move(Location((0, -40, 152.5)))
        front_plate.label = "front-plate"
        children.append(front_plate)

        super().__init__(
            label=label,
            color=color,
            material=material,
            parent=parent,
            children=children,
        )
