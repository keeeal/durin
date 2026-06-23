from copy import copy

from build123d import *
from build123d.topology.shape_core import Shape

from cad.bearing import CustomCappedBearing
from cad.utils.color import unset_color


class Bed(BasePartObject):
    def __init__(
        self,
        width: float,
        num_slots: int,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] | None = None,
        mode: Mode = Mode.ADD,
    ) -> None:
        with BuildSketch() as slot:
            with BuildLine():
                Polyline(
                    (0.0, 0.0),
                    (4.0, 0.0),
                    (4.0, 4.0),
                    (6.5, 4.0),
                    (6.5, 2.5),
                    (11.5, 2.5),
                    (11.5, 5.5),
                    (7.5, 8.5),
                    (7.5, 11.5),
                    (4.0, 11.5),
                    (2.0, 13.0),
                    (0.0, 13.0),
                )
                mirror(about=Plane.YZ)
            make_face()

        with BuildSketch() as end_slot:
            with BuildLine():
                Polyline(
                    (0.0, 4.0),
                    (2.5, 4.0),
                    (2.5, 2.5),
                    (7.5, 2.5),
                    (7.5, 4.0),
                    (11.5, 4.0),
                    (11.5, 5.5),
                    (7.5, 8.5),
                    (7.5, 12.5),
                    (2.5, 12.5),
                    (2.5, 11.0),
                    (0.0, 11.0),
                )
                mirror(about=Plane.YZ)
            make_face()

        with BuildPart() as main:
            with BuildSketch(Plane.YZ) as profile:
                Rectangle(22.5 * (num_slots + 1), 15, align=Align.MIN)
                with Locations(
                    *(
                        Location((22.5 * index, 15 * (index % 2)), angle=180 * index)
                        for index in range(1, num_slots + 1)
                    ),
                ):
                    add(slot, mode=Mode.SUBTRACT)
                index = num_slots + 1
                with Locations(
                    Location((0, 0), angle=0),
                    Location((22.5 * index, 15 * (index % 2)), angle=180 * index),
                ):
                    add(end_slot, mode=Mode.SUBTRACT)
                fillet(profile.vertices(), radius=0.5)
            extrude(amount=width)

        super().__init__(main.part, rotation=rotation, align=align, mode=mode)


class BedBearingMount(BasePartObject):
    def __init__(
        self,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] | None = None,
        mode: Mode = Mode.ADD,
    ) -> None:
        with BuildPart() as main:
            with BuildSketch(Plane.XZ) as profile:
                RegularPolygon(radius=14, side_count=10)
                with Locations((-12.25, 0), (+12.25, 0)):
                    Rectangle(3.5, 22, align=(Align.CENTER, Align.MIN))
                with Locations((0, 22)):
                    Rectangle(49.5, 3.5, align=(Align.CENTER, Align.MAX))
                Circle(9.5, mode=Mode.SUBTRACT)
                fillet(profile.vertices().group_by(Axis.Y)[:-2], radius=1.0)
            extrude(amount=15, both=True)
            with (
                BuildSketch(),
                GridLocations(
                    x_spacing=38,
                    y_spacing=10,
                    x_count=2,
                    y_count=2,
                ),
            ):
                Circle(2.75)
            extrude(until=Until.LAST, mode=Mode.SUBTRACT)

        super().__init__(main.part, rotation=rotation, align=align, mode=mode)


class BedThreadMount(BasePartObject):
    def __init__(
        self,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] | None = None,
        mode: Mode = Mode.ADD,
    ) -> None:
        with BuildPart() as main:
            with BuildSketch(Plane.XZ) as profile:
                RegularPolygon(radius=11, side_count=10)
                with Locations((-9.25, 0), (+9.25, 0)):
                    Rectangle(3.5, 22, align=(Align.CENTER, Align.MIN))
                with Locations((0, 22)):
                    Rectangle(44.5, 3.5, align=(Align.CENTER, Align.MAX))
                Circle(4.25, mode=Mode.SUBTRACT)
                fillet(profile.vertices().group_by(Axis.Y)[:-2], radius=1.0)
            extrude(amount=15, both=True)
            with (
                BuildSketch(),
                GridLocations(
                    x_spacing=33,
                    y_spacing=10,
                    x_count=2,
                    y_count=3,
                ),
            ):
                Circle(2.75)
            extrude(until=Until.LAST, mode=Mode.SUBTRACT)
            with BuildSketch(), Locations((0, -15)):
                Rectangle(10, 10)
            extrude(amount=12, both=True, mode=Mode.SUBTRACT)
            with BuildSketch(Plane.XY.move(Location((0, 0, 22)))):
                with Locations((0, -12.5)):
                    Rectangle(15, 10)
            extrude(amount=-3.5, mode=Mode.SUBTRACT)
            with BuildSketch(Plane.XZ.move(Location((0, -15, 0)))):
                RegularPolygon(radius=9.5, side_count=6, rotation=30)
            extrude(amount=-10, mode=Mode.SUBTRACT)

        super().__init__(main.part, rotation=rotation, align=align, mode=mode)


class BedAssembly(Compound):
    def __init__(
        self,
        *,
        label: str = "",
        color: Color | None = None,
        material: str = "",
        parent: Compound | None = None,
    ) -> None:
        children: list[Shape] = []

        bed = Bed(width=300, num_slots=7, align=(Align.CENTER, Align.CENTER, Align.MIN))
        bed.label = "bed"
        children.append(bed)

        bearing_mount = BedBearingMount(align=(Align.CENTER, Align.CENTER, Align.MAX))
        bearing_mounts = [
            copy(bearing_mount).move(Location((-100, -40, 0))),
            copy(bearing_mount).move(Location((+100, -40, 0))),
            copy(bearing_mount).move(Location((-100, +40, 0))),
            copy(bearing_mount).move(Location((+100, +40, 0))),
        ]
        for index, mount in enumerate(bearing_mounts):
            mount.label = f"bearing-mount-{index}"
        children.extend(bearing_mounts)

        large_bearing = CustomCappedBearing(
            inner_diameter=10,
            outer_diameter=19,
            thickness=5,
        )
        bearings = [
            copy(large_bearing).move(Location((-100, -50, -22), (90, 0, 0))),
            copy(large_bearing).move(Location((-100, -25, -22), (90, 0, 0))),
            copy(large_bearing).move(Location((+100, -50, -22), (90, 0, 0))),
            copy(large_bearing).move(Location((+100, -25, -22), (90, 0, 0))),
            copy(large_bearing).move(Location((-100, +50, -22), (-90, 0, 0))),
            copy(large_bearing).move(Location((-100, +25, -22), (-90, 0, 0))),
            copy(large_bearing).move(Location((+100, +50, -22), (-90, 0, 0))),
            copy(large_bearing).move(Location((+100, +25, -22), (-90, 0, 0))),
        ]
        for index, bearing in enumerate(bearings):
            unset_color(bearing)
            bearing.label = f"bearing-{index}"
        children.extend(bearings)

        thread_mount = BedThreadMount(align=(Align.CENTER, Align.CENTER, Align.MAX))
        thread_mount.label = "thread-mount"
        children.append(thread_mount)

        super().__init__(
            label=label,
            color=color,
            material=material,
            parent=parent,
            children=children,
        )
