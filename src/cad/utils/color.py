from build123d.topology.shape_core import Shape


def unset_color(shape: Shape) -> Shape:
    shape.color = None
    for child in shape.children:
        if isinstance(child, Shape):
            unset_color(child)
    return shape
