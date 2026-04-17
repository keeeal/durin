from copy import copy

from bd_warehouse.open_builds import StepperMotor
from build123d import *
from build123d.topology.shape_core import Shape

from cad.lead_screw import BrassNut, LeadScrew, LeadScrewJoiner
from cad.linear_rail import EG15LinearBearing, MGN15LinearRail
from cad.spindle import SpindleAssembly
from cad.utils.color import unset_color
from cad.utils.env import SIMPLE, Z


class ThreadBlock(BasePartObject):
    def __init__(
        self,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] | None = None,
        mode: Mode = Mode.ADD,
    ) -> None:
        with BuildPart() as main:
            with BuildSketch():
                Rectangle(33.25, 9, align=(Align.MIN, Align.MIN))
                Rectangle(33.25, 13, align=(Align.MAX, Align.MIN))
                Rectangle(32, 50, align=(Align.CENTER, Align.MIN))
            extrude(amount=11.5, both=True)
            with BuildSketch(Plane.XZ):
                with Locations((-23, 0), (+23, 0)):
                    Circle(3)
            extrude(until=Until.FIRST, mode=Mode.SUBTRACT)
            with BuildSketch(Plane.YZ):
                with Locations((34.5, 0)):
                    Circle(5)
            extrude(until=Until.LAST, both=True, mode=Mode.SUBTRACT)
            chamfer(main.edges(), length=0.5)

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
            with BuildSketch(Plane.XZ):
                with Locations((0, 23)):
                    RectangleRounded(85, 150, radius=2)
                    with GridLocations(
                        x_spacing=70,
                        y_spacing=40,
                        x_count=2,
                        y_count=4,
                    ):
                        Circle(1.75, mode=Mode.SUBTRACT)
                with Locations((0, -35), (0, +35)):
                    with GridLocations(
                        x_spacing=26,
                        y_spacing=26,
                        x_count=2,
                        y_count=2,
                    ):
                        Circle(2.25, mode=Mode.SUBTRACT)
                with Locations((-23, 1), (+23, 1)):
                    SlotOverall(9, 5.5, rotation=90, mode=Mode.SUBTRACT)
            extrude(amount=3)

            with BuildSketch(Plane.YZ):
                with BuildLine():
                    Polyline(
                        (-3, 72),
                        (-3, 98),
                        (-35, 75),
                        (-35, 72),
                        close=True,
                    )
                make_face()
            extrude(amount=25, both=True)

            with BuildSketch(Plane.XY.move(Location((0, 0, 75)))):
                Rectangle(43, 100)
            extrude(until=Until.LAST, mode=Mode.SUBTRACT)
            with BuildSketch(Plane.XY.move(Location((0, 0, 75)))):
                with Locations((0, -13.75)):
                    Circle(12.5)
                    with Locations(
                        Location((-15.5, -15.5)),
                        Location((+15.5, -15.5)),
                    ):
                        Circle(1.75)
            extrude(amount=-3, mode=Mode.SUBTRACT)

        super().__init__(main.part, rotation=rotation, align=align, mode=mode)


class StepperMotorBracket(BasePartObject):
    def __init__(
        self,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] | None = None,
        mode: Mode = Mode.ADD,
    ) -> None:
        with BuildPart() as main:
            with BuildSketch() as profile:
                Rectangle(50, 53, align=(Align.CENTER, Align.MIN))
                with Locations((0, 27)):
                    with GridLocations(
                        x_spacing=30,
                        y_spacing=0,
                        x_count=2,
                        y_count=1,
                    ):
                        SlotOverall(34, 4, rotation=90, mode=Mode.SUBTRACT)
                chamfer(profile.vertices().group_by(Axis.Y)[-1], length=5)
            extrude(amount=3)
            with BuildSketch(Plane.XZ) as profile:
                Rectangle(50, 51, align=(Align.CENTER, Align.MIN))
                with Locations((0, 30)):
                    Circle(11, mode=Mode.SUBTRACT)
                    with GridLocations(
                        x_spacing=31,
                        y_spacing=31,
                        x_count=2,
                        y_count=2,
                    ):
                        Circle(1.75, mode=Mode.SUBTRACT)
                chamfer(profile.vertices().group_by(Axis.Y)[-1], length=5)
            extrude(amount=-3)

        super().__init__(main.part, rotation=rotation, align=align, mode=mode)


class StepperMotorPlate(BasePartObject):
    def __init__(
        self,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] | None = None,
        mode: Mode = Mode.ADD,
    ) -> None:
        with BuildPart() as main:
            with BuildSketch():
                RectangleRounded(39.5, 82, radius=4.6, align=(Align.CENTER, Align.MIN))
                with Locations((0, 21.25)):
                    Circle(12.5, mode=Mode.SUBTRACT)
                    with Locations(
                        Location((-14.25, -14.25), 45),
                        Location((+14.25, -14.25), -45),
                        Location((-14.25, +14.25), -45),
                        Location((+14.25, +14.25), 45),
                    ):
                        SlotOverall(6.65, 3.1, mode=Mode.SUBTRACT)
                with Locations((0, 63.8)):
                    with GridLocations(
                        x_spacing=10,
                        y_spacing=20,
                        x_count=3,
                        y_count=2,
                    ):
                        Circle(2.5, mode=Mode.SUBTRACT)
            extrude(amount=3)

        super().__init__(main.part, rotation=rotation, align=align, mode=mode)


class GantryAssembly(Compound):
    def __init__(
        self,
        *,
        label: str = "",
        color: Color | None = None,
        material: str = "",
        parent: Compound | None = None,
    ):
        children: list[Shape] = []

        eg15_bearing = EG15LinearBearing()
        eg15_bearings = [
            copy(eg15_bearing).move(Location((0, 0, 210), (0, 90, 180))),
            copy(eg15_bearing).move(Location((0, 0, 140), (0, 90, 180))),
        ]
        for index, eg15_bearing in enumerate(eg15_bearings):
            eg15_bearing.label = f"eg15-bearing-{index}"
        children.extend(eg15_bearings)

        thread_block = ThreadBlock().move(Location((0, -20.25, 176)))
        thread_block.label = "thread-block"
        children.append(thread_block)

        brass_nut = BrassNut().move(Location((-16, 14.25, 176), (0, -90, 0)))
        brass_nut.label = "brass-nut"
        children.append(brass_nut)

        back_plate = BackPlate().move(Location((0, -20.25, 175)))
        back_plate.label = "back-plate"
        children.append(back_plate)

        # stepper_motor_bracket = StepperMotorBracket().move(
        #     Location((0, -22.5, 250), (90, 0, 180)),
        # )
        # stepper_motor_bracket.label = "stepper-motor-bracket"
        # children.append(stepper_motor_bracket)

        # stepper_motor_plate = StepperMotorPlate().move(
        #     Location((0, -55.25, 247)),
        # )
        # stepper_motor_plate.label = "stepper-motor-plate"
        # children.append(stepper_motor_plate)

        stepper_motor = StepperMotor("Nema17").move(
            Location((0, -34, 250), (180, 0, 0))
        )
        unset_color(stepper_motor)
        stepper_motor.label = "stepper-motor"
        children.append(stepper_motor)

        joiner = LeadScrewJoiner().move(
            Location((0, -34, 234)),
        )
        joiner.label = "lead-screw-joiner"
        children.append(joiner)

        lead_screw = LeadScrew(length=80, simple=SIMPLE).move(
            Location((0, -34, 225), (180, 0, 0)),
        )
        lead_screw.label = "lead-screw"
        children.append(lead_screw)

        mgn15_rails = [
            MGN15LinearRail(
                length=150, align=(Align.CENTER, Align.MIN, Align.CENTER)
            ).move(
                Location((-35, -23.25, 198), 180),
            ),
            MGN15LinearRail(
                length=150, align=(Align.CENTER, Align.MIN, Align.CENTER)
            ).move(
                Location((+35, -23.25, 198), 180),
            ),
        ]
        for index, mgn15_rail in enumerate(mgn15_rails):
            mgn15_rail.label = f"mgn15-rail-{index}"
        children.extend(mgn15_rails)

        # rail = VSlotLinearRail("20x20", length=90, align=Align.CENTER).move(
        #     Location((0, -9, 237), (0, 90, 0)),
        # )
        # unset_color(rail)
        # rail.label = "v-slot-rail"
        # children.append(rail)

        spindle_assembly = SpindleAssembly().move(Location((0, 0.75, Z)))
        spindle_assembly.label = "spindle-assembly"
        children.append(spindle_assembly)

        super().__init__(
            label=label,
            color=color,
            material=material,
            parent=parent,
            children=children,
        )
