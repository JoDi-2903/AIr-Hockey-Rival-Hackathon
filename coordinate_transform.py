"""Transform between the coordinate systems of Field, MCS and Camera."""

# Offsets field origin by 5.5mm in X and 6.5mm in Y.
X_OFFSET_MCS = 5.5
Y_OFFSET_MCS = 6.5

def field_to_machine_coordinates(pos_field: tuple[float, float]) -> tuple[float, float]:
    """
    Convert field coordinates to machine coordinates.

    :param pos_field: Field coordinates.
    :return: Machine coordinates.
    """
    x, y = pos_field
    return x - X_OFFSET_MCS, y - Y_OFFSET_MCS

def machine_to_field_coordinates(pos_mcs: tuple[float, float]) -> tuple[float, float]:
    """
    Convert machine coordinates to field coordinates.
    
    :param pos_mcs: Machine coordinates.
    :return: Field coordinates.
    """
    x, y = pos_mcs
    return x + X_OFFSET_MCS, y + Y_OFFSET_MCS