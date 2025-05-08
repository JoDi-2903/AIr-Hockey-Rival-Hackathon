from typing import Tuple

X_OFFSET = 5.5
Y_OFFSET = 6.5

def field_to_machine_coordinates(pos: Tuple[float, float]) -> Tulpe[float, float]:
    """
    Convert field coordinates to machine coordinates.
    Offsets field origin by 5.5mm in X and 6.5mm in Y.
    """
    x, y = pos
    return x -X_OFFSET, y - Y_OFFSET

def machine_to_field_coordinates(pos: Tuple[float, float]) -> Tulpe[float, float]
    """
    Convert machine coordinates to field coordinates.
    Adds the Offset to the field origin.
    """
    x, y = pos
    return x + X_OFFSET, y + Y_OFFSET