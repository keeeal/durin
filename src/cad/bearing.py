from bd_warehouse.bearing import SingleRowCappedDeepGrooveBallBearing


class CustomCappedBearing(SingleRowCappedDeepGrooveBallBearing):
    def __init__(
        self,
        inner_diameter: float,
        outer_diameter: float,
        thickness: float,
    ):
        delta = outer_diameter - inner_diameter
        self.bearing_data = {
            "M": {
                "SKT:d": str(inner_diameter),
                "SKT:D": str(outer_diameter),
                "SKT:B": str(thickness),
                "SKT:d1": str(inner_diameter + delta / 4),
                "SKT:D1": str(outer_diameter - delta / 4),
                "SKT:r12": str(delta / 64),
            }
        }
        super().__init__("M")
