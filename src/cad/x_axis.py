from copy import copy

from bd_warehouse.bearing import SingleRowCappedDeepGrooveBallBearing
from bd_warehouse.open_builds import StepperMotor, VSlotLinearRail
from build123d import *
from build123d.topology.shape_core import Shape

from cad.gantry import GantryAssembly
from cad.lead_screw import LeadScrew
from cad.linear_rail import EG15LinearRail
from cad.utils.color import unset_color
from cad.utils.env import SIMPLE, X


class SidePlate(BasePartObject):
    def __init__(
        self,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] | None = None,
        mode: Mode = Mode.ADD,
    ) -> None:
        with BuildPart() as main:
            with BuildSketch() as profile:
                with BuildLine():
                    Polyline(
                        (0, 0),
                        (50, 0),
                        (110, 50),
                        (220, 50),
                        (220, 110),
                        (70, 110),
                        (50, 95),
                        (0, 95),
                        close=True,
                    )
                make_face()
                fillet(
                    profile.vertices().group_by(Axis.X)[1:-1],
                    radius=20,
                )
                chamfer(
                    profile.vertices().group_by(Axis.X)[-1].group_by(Axis.Y)[0],
                    length=12,
                    length2=8,
                )
                chamfer(
                    profile.vertices().group_by(Axis.X)[0]
                    + profile.vertices().group_by(Axis.X)[-1].group_by(Axis.Y)[-1],
                    length=2,
                )
                with Locations((20, 47.5)):
                    with GridLocations(
                        x_spacing=20,
                        y_spacing=37.5,
                        x_count=2,
                        y_count=3,
                    ):
                        Circle(2.75, mode=Mode.SUBTRACT)
                with Locations(
                    (210, 98),
                    (133, 98),
                    (135, 71),
                    (205, 71),
                ):
                    Circle(2.75, mode=Mode.SUBTRACT)
            extrude(amount=15)
            chamfer(main.edges().group_by(Axis.Z)[-1], length=0.5)

        super().__init__(main.part, rotation=rotation, align=align, mode=mode)


class LeftPlate(BasePartObject):
    def __init__(
        self,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] | None = None,
        mode: Mode = Mode.ADD,
    ) -> None:
        with BuildPart() as main:
            SidePlate(align=(Align.MIN, Align.MIN, Align.CENTER))
            with BuildSketch():
                with Locations((171, 71)):
                    Circle(4.75)
            extrude(until=Until.FIRST, mode=Mode.SUBTRACT)
            with BuildSketch():
                with Locations((171, 71)):
                    Circle(8)
            extrude(until=Until.LAST, mode=Mode.SUBTRACT)
            chamfer(main.edges(Select.LAST).group_by(Axis.Z)[-1], length=0.5)

        super().__init__(main.part, rotation=rotation, align=align, mode=mode)


class RightPlate(BasePartObject):
    def __init__(
        self,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] | None = None,
        mode: Mode = Mode.ADD,
    ) -> None:
        with BuildPart() as main:
            SidePlate()
            with BuildSketch():
                with Locations((171, 71)):
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


class XAxisAssembly(Compound):
    def __init__(
        self,
        *,
        label: str = "",
        color: Color | None = None,
        material: str = "",
        parent: Compound | None = None,
    ):
        children: list[Shape] = []

        left_plate = LeftPlate(align=Align.MIN).move(
            Location((-185, 0, 5), (0, -90, 0)),
        )
        left_plate.label = "left-plate"
        children.append(left_plate)

        right_plate = (
            RightPlate(align=Align.MIN)
            .mirror()
            .move(
                Location((+185, 0, 5), (0, -90, 0)),
            )
        )
        right_plate.label = "right-plate"
        children.append(right_plate)

        rail = VSlotLinearRail("20x20", length=370, align=Align.CENTER)
        rails = [
            copy(rail).move(Location((0, 71, 210), (0, 90, 0))),
            copy(rail).move(Location((0, 71, 140), (0, 90, 0))),
        ]
        for index, rail in enumerate(rails):
            unset_color(rail)
            rail.label = f"rail-{index}"
        children.extend(rails)

        rods = [
            Cylinder(radius=5, height=370, align=Align.CENTER).move(
                Location((0, 98, 138), (0, 90, 0)),
            ),
            Cylinder(radius=5, height=370, align=Align.CENTER).move(
                Location((0, 98, 215), (0, 90, 0)),
            ),
        ]
        for index, rod in enumerate(rods):
            rod.label = f"rod-{index}"
        children.extend(rods)

        bearing = SingleRowCappedDeepGrooveBallBearing("M8-16-5").move(
            Location((-200, 71, 176), (0, 90, 0)),
        )
        unset_color(bearing)
        bearing.label = f"bearing"
        children.append(bearing)

        stepper_motor = StepperMotor("Nema17").move(
            Location((200, 71, 176), (0, -90, 0)),
        )
        unset_color(stepper_motor)
        stepper_motor.label = "stepper-motor"
        children.append(stepper_motor)

        lead_screw = LeadScrew(length=400, simple=SIMPLE).move(
            Location((175, 71, 176), (0, -90, 0)),
        )
        lead_screw.label = "lead-screw"
        children.append(lead_screw)

        linear_rail = EG15LinearRail(
            length=330, align=(Align.CENTER, Align.MIN, Align.CENTER)
        )
        linear_rails = [
            copy(linear_rail).move(Location((0, 61, 210), (0, 90, 180))),
            copy(linear_rail).move(Location((0, 61, 140), (0, 90, 180))),
        ]
        for index, linear_rail in enumerate(linear_rails):
            linear_rail.label = f"linear-rail-{index}"
        children.extend(linear_rails)

        gantry = GantryAssembly().move(
            Location((X, 56.75, 0), (0, 0, 0)),
        )
        gantry.label = "gantry"
        children.append(gantry)

        super().__init__(
            label=label,
            color=color,
            material=material,
            parent=parent,
            children=children,
        )
