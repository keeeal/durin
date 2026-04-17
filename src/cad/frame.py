from copy import copy
from itertools import product

from bd_warehouse.bearing import SingleRowCappedDeepGrooveBallBearing
from bd_warehouse.fastener import SocketHeadCapScrew
from bd_warehouse.open_builds import StepperMotor, VSlotLinearRail
from build123d import *
from build123d.topology.shape_core import Shape

from cad.lead_screw import LeadScrew
from cad.utils.color import unset_color
from cad.utils.env import SIMPLE
from cad.utils.math import float_range, polar_to_cartesian


class BasePlate(BasePartObject):
    def __init__(
        self,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] | None = None,
        mode: Mode = Mode.ADD,
    ) -> None:
        with BuildPart() as main:
            with BuildSketch() as profile:
                RectangleRounded(370, 45, 1)
                with Locations((0, -22.5)):
                    Rectangle(270, 6, mode=Mode.SUBTRACT)
                fillet(profile.vertices(Select.LAST), radius=1.5)
                with Locations(
                    (-175, 12.5),
                    (+175, 12.5),
                    (-175, -7.5),
                    (+175, -7.5),
                    (-100, 1.5),
                    (+100, 1.5),
                ):
                    Circle(2.75, mode=Mode.SUBTRACT)
            extrude(amount=10)
            chamfer(main.edges().group_by(Axis.Z)[-1], length=0.5)

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
            BasePlate(align=Align.CENTER)
            with BuildSketch():
                with Locations((0, 1.5)):
                    Circle(4.5)
            extrude(until=Until.FIRST, mode=Mode.SUBTRACT)
            with BuildSketch():
                with Locations((0, 1.5)):
                    Circle(8)
            extrude(until=Until.LAST, mode=Mode.SUBTRACT)
            chamfer(main.edges(Select.LAST).group_by(Axis.Z)[-1], length=0.5)

        super().__init__(main.part, rotation=rotation, align=align, mode=mode)


class BackPlate(BasePartObject):
    def __init__(
        self,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] | None = None,
        mode: Mode = Mode.ADD,
    ) -> None:
        with BuildPart() as main:
            BasePlate()
            with BuildSketch():
                with Locations((0, 1.5)):
                    Circle(12)
                    with GridLocations(
                        x_spacing=31,
                        y_spacing=31,
                        x_count=2,
                        y_count=2,
                    ):
                        Circle(2)
            extrude(until=Until.LAST, mode=Mode.SUBTRACT)
            chamfer(main.edges(Select.LAST).group_by(Axis.Z)[-1], length=0.5)

        super().__init__(main.part, rotation=rotation, align=align, mode=mode)


class Knob(BasePartObject):
    def __init__(
        self,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] | None = None,
        mode: Mode = Mode.ADD,
    ) -> None:
        outer_radius = 9
        num_points = 56

        with BuildPart() as main:
            Cylinder(outer_radius, 10, align=(Align.CENTER, Align.CENTER, Align.MIN))
            chamfer(main.edges(), length=0.5)
            with BuildSketch() as profile:
                with BuildLine():
                    Polyline(
                        *(
                            polar_to_cartesian(outer_radius - 0.25 * (index % 2), angle)
                            for index, angle in enumerate(
                                float_range(0, 360, 180 / num_points)
                            )
                        ),
                        close=True,
                    )
                make_face()
            extrude(amount=10, mode=Mode.INTERSECT)
            Cylinder(7.5, 18, align=(Align.CENTER, Align.CENTER, Align.MIN))
            with Locations((0, 0, 6)):
                Cylinder(
                    4,
                    18,
                    align=(Align.CENTER, Align.CENTER, Align.MIN),
                    mode=Mode.SUBTRACT,
                )
            chamfer(main.edges().group_by(Axis.Z)[-1], length=0.5)
            with BuildSketch(Plane.YZ):
                with Locations((0, 13)):
                    Circle(2)
            extrude(until=Until.FIRST, mode=Mode.SUBTRACT)
            chamfer(main.edges(Select.LAST), length=0.5)

        super().__init__(main.part, rotation=rotation, align=align, mode=mode)


class EndStop(BasePartObject):
    def __init__(
        self,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] | None = None,
        mode: Mode = Mode.ADD,
    ) -> None:
        with BuildPart() as main:
            with BuildSketch(Plane.XZ):
                with Locations((5, 0)):
                    Rectangle(7.5, 1, align=Align.MIN)
                with Locations((6, 7)):
                    Circle(1)
                with Locations((9, 5)):
                    Circle(3)
                make_hull()
                with Locations((2, 0)):
                    Rectangle(10, 4, align=Align.MIN)
            revolve()

        super().__init__(main.part, rotation=rotation, align=align, mode=mode)


class CornerBracket(BasePartObject):
    def __init__(
        self,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] | None = None,
        mode: Mode = Mode.ADD,
    ) -> None:
        with BuildPart() as main:
            Box(20, 5, 20)
            chamfer(main.edges(), length=0.5)

        super().__init__(main.part, rotation=rotation, align=align, mode=mode)


class JoiningPlate(BasePartObject):
    def __init__(
        self,
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
                        (60, 0),
                        (60, 20),
                        (20, 60),
                        (0, 60),
                        close=True,
                    )
                make_face()
                with Locations(
                    *(
                        (20 * i + 10, 20 * j + 10)
                        for i, j in product(range(3), range(3))
                        if i == 0 or j == 0
                    )
                ):
                    Circle(2.5, mode=Mode.SUBTRACT)
            extrude(amount=4)

        super().__init__(main.part, rotation=rotation, align=align, mode=mode)


class FrameAssembly(Compound):
    def __init__(
        self,
        *,
        label: str = "",
        color: Color | None = None,
        material: str = "",
        parent: Compound | None = None,
    ):
        children: list[Shape] = []

        rails = [
            VSlotLinearRail("20x20", length=290).move(
                Location((-195, -10, 0), (0, 0, 0)),
            ),
            VSlotLinearRail("20x20", length=290).move(
                Location((+195, -10, 0), (0, 0, 0)),
            ),
            VSlotLinearRail("20x40", length=295).move(
                Location((-175, 0, 25), (90, 0, 0)),
            ),
            VSlotLinearRail("20x40", length=295).move(
                Location((+175, 0, 25), (90, 0, 0)),
            ),
            VSlotLinearRail("20x40", length=290).move(
                Location((-195, -275, 0), (0, 0, 0)),
            ),
            VSlotLinearRail("20x40", length=290).move(
                Location((+195, -275, 0), (0, 0, 0)),
            ),
            VSlotLinearRail("20x20", length=290).move(
                Location((-195, -5, 300), (90, 0, 0)),
            ),
            VSlotLinearRail("20x20", length=290).move(
                Location((+195, -5, 300), (90, 0, 0)),
            ),
            VSlotLinearRail("20x20", length=370, align=Align.CENTER).move(
                Location((0, -10, 300), (0, 90, 0)),
            ),
        ]
        for index, rail in enumerate(rails):
            unset_color(rail)
            rail.label = f"rail-{index}"
        children.extend(rails)

        front_plate = FrontPlate(
            align=(Align.CENTER, Align.MIN, Align.MIN),
        ).move(
            Location((0, -295, 0), (90, 0, 0)),
        )
        front_plate.label = "front-plate"
        children.append(front_plate)

        back_plate = BackPlate(
            align=(Align.CENTER, Align.MAX, Align.MIN),
        ).move(
            Location((0, 0, 45), (-90, 0, 180)),
        )
        back_plate.label = "back-plate"
        children.append(back_plate)

        screw = SocketHeadCapScrew("M5-0.8", length=15, simple=SIMPLE)
        unset_color(screw)
        screws = [
            copy(screw).move(Location((-175, 10, 15), (-90, 0, 0))),
            copy(screw).move(Location((+175, 10, 15), (-90, 0, 0))),
            copy(screw).move(Location((-175, 10, 35), (-90, 0, 0))),
            copy(screw).move(Location((+175, 10, 35), (-90, 0, 0))),
            copy(screw).move(Location((-100, 10, 24), (-90, 0, 0))),
            copy(screw).move(Location((+100, 10, 24), (-90, 0, 0))),
            copy(screw).move(Location((-175, -305, 15), (90, 0, 0))),
            copy(screw).move(Location((+175, -305, 15), (90, 0, 0))),
            copy(screw).move(Location((-175, -305, 35), (90, 0, 0))),
            copy(screw).move(Location((+175, -305, 35), (90, 0, 0))),
            copy(screw).move(Location((-100, -305, 24), (90, 0, 0))),
            copy(screw).move(Location((+100, -305, 24), (90, 0, 0))),
        ]
        for index, screw in enumerate(screws):
            screw.label = f"screw-{index}"
        children.extend(screws)

        bed_rails = [
            Cylinder(
                radius=5,
                height=295,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).move(Location((-100, 0, 24), (90, 0, 0))),
            Cylinder(
                radius=5,
                height=295,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).move(Location((+100, 0, 24), (90, 0, 0))),
        ]
        for index, bed_rail in enumerate(bed_rails):
            bed_rail.label = f"bed-rail-{index}"
        children.extend(bed_rails)

        lead_screw = LeadScrew(length=300, simple=SIMPLE).move(
            Location((0, -15, 24), (90, 0, 0)),
        )
        lead_screw.label = "lead-screw"
        children.append(lead_screw)

        stepper_motor = StepperMotor("Nema17").move(
            Location((0, 10, 24), (90, 0, 0)),
        )
        unset_color(stepper_motor)
        stepper_motor.label = "stepper-motor"
        children.append(stepper_motor)

        bearing = SingleRowCappedDeepGrooveBallBearing("M8-16-5").move(
            Location((0, -300, 24), (90, 0, 0)),
        )
        unset_color(bearing)
        bearing.label = f"bearing"
        children.append(bearing)

        knob = Knob(align=(Align.CENTER, Align.CENTER, Align.MAX)).move(
            Location((0, -305, 24), (-90, 0, 0)),
        )
        knob.label = "knob"
        children.append(knob)

        foot = EndStop()
        feet = [
            copy(foot).move(Location((-195, -10, 0), (180, 0, 0))),
            copy(foot).move(Location((+195, -10, 0), (180, 0, 0))),
            copy(foot).move(Location((-195, -265, 0), (180, 0, 0))),
            copy(foot).move(Location((+195, -265, 0), (180, 0, 0))),
        ]
        for index, foot in enumerate(feet):
            foot.label = f"foot-{index}"
        children.extend(feet)

        corner_bracket = CornerBracket()
        corner_brackets = [
            copy(corner_bracket).move(Location((-195, -2.5, 300))),
            copy(corner_bracket).move(Location((+195, -2.5, 300))),
        ]
        for index, corner_bracket in enumerate(corner_brackets):
            corner_bracket.label = f"corner-bracket-{index}"
        children.extend(corner_brackets)

        joining_plate = JoiningPlate()
        joining_plates = [
            copy(joining_plate).move(Location((-205, -295, 310), (0, -90, 90))),
            copy(joining_plate).move(Location((+205, -295, 310), (0, 90, 0))),
        ]
        for index, joining_plate in enumerate(joining_plates):
            joining_plate.label = f"joining-plate-{index}"
        children.extend(joining_plates)

        super().__init__(
            label=label,
            color=color,
            material=material,
            parent=parent,
            children=children,
        )
