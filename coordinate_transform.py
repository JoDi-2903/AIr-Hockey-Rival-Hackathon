"""Transform between the coordinate systems of Field, MCS and Camera."""

# Offsets field origin by 5.5mm in X and 6.5mm in Y.
X_OFFSET_MCS = 67 - 20
Y_OFFSET_MCS = 75 - 20

def field_to_machine_coordinates(pos_field: tuple[float, float]) -> tuple[float, float]:
    """
    Convert field coordinates to machine coordinates.

    :param pos_field: Field coordinates in millimeters.
    :return: Machine coordinates in millimeters.
    """
    x, y = pos_field
    return x - X_OFFSET_MCS, y - Y_OFFSET_MCS

def machine_to_field_coordinates(pos_mcs: tuple[float, float]) -> tuple[float, float]:
    """
    Convert machine coordinates to field coordinates.
    
    :param pos_mcs: Machine coordinates in millimeters.
    :return: Field coordinates in millimeters.
    """
    x, y = pos_mcs
    return x + X_OFFSET_MCS, y + Y_OFFSET_MCS


def camera_to_field_coordinates(pos_camera: tuple[float, float]) -> tuple[float, float]:
    """
    Convert a camera position in pixels to field coordinates in millimeters.

    :param pos_camera: A tuple (x_px, y_px) representing the position in camera pixels.
    :return: A tuple (x_mm, y_mm) representing the position on the field in millimeters,
             with origin at (0,0) defined by the measured pixel origin.
    """
    # Pixel coordinates of the field origin (0,0) in the camera image
    origin_px = (68.0, 30.0)

    # Conversion factor from pixels to millimeters (same for X and Y)
    # Measurements:
    # Puck pos1: x=322 y=127 in px  # closer to origin edge
    # Puck pos2: x=314 y=543 in px
    # Both positions have a distance in y-direction of 340mm
    # 416 px in the measurement correspond to 340 mm => ~1.224 px per mm
    px_per_mm = 416.0 / 340.0

    # Compute pixel offsets relative to the field origin
    delta_x_px = pos_camera[0] - origin_px[0]
    delta_y_px = pos_camera[1] - origin_px[1]

    # Convert pixel offsets to millimeters
    x_mm = delta_x_px / px_per_mm
    y_mm = delta_y_px / px_per_mm

    return x_mm, y_mm
