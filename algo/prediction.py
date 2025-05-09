import copy

from algo.model import Entity, Field, Vec

def predict_offence_pos(entity: Entity, field: Field, x_pos_offence) -> tuple[Vec, Vec]:
    """Predict the position and velocity of the puck for a given x coordinate.
    Raises ValueError if the velocity in x direction is zero.
    """
    if entity.v.x == 0:
        raise ValueError("Velocity in x direction is zero, cannot predict position.")

    # Calculate the time it would take to reach the given x coordinate
    time_to_reach_x = (x_pos_offence - entity.pos.x) / entity.v.x

    # Calculate the new position and velocity after that time
    pos, v = predict(entity, field, time_to_reach_x)

    # Set the x coordinate to the given value
    pos.x = x_pos_offence

    return pos, v


def predict(entity: Entity, field: Field, dt: float) -> tuple[Vec, Vec]:
    min_border = min(field.w, field.h)
    small_dt = min_border / entity.v.abs()
    # print(dt, small_dt)

    pos = copy.copy(entity.pos)
    # print(pos)
    v = copy.copy(entity.v)
    dt_until_now = 0

    while dt_until_now < dt:
        this_dt = min(small_dt, dt - dt_until_now)
        # Update position based on velocity
        pos.x += v.x * this_dt
        pos.y += v.y * this_dt
        # print(pos)

        # Check for collisions with the vertical walls (x-axis)
        if pos.x - entity.radius < 0:
            v.x *= -1 # Reverse velocity in x direction
            pos.x += 2*(0 + entity.radius - pos.x) # mirror location at virtual boarder

        if pos.x + entity.radius > field.w:
            v.x *= -1 # Reverse velocity in x direction
            pos.x += 2*((field.w - entity.radius) - pos.x) # mirror location at virtual boarder

        # Check for collisions with the vertical walls (x-axis)
        if pos.y - entity.radius < 0:
            v.y *= -1 # Reverse velocity in x direction
            pos.y += 2*(0 + entity.radius - pos.y) # mirror location at virtual boarder

        if pos.y + entity.radius > field.h:
            v.y *= -1 # Reverse velocity in x direction
            pos.y += 2*((field.h - entity.radius) - pos.y) # mirror location at virtual boarder

        dt_until_now += this_dt

    return pos, v
