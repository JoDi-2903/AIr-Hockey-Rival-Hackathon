from algo.model import Entity, Field, Vec
from algo.prediction import predict_offence_pos_time
from algo.constants import ROBOT_SPEED

time_tolerance = 30 * 1e-3  # ms, tolerance for time prediction

def predict_save_shot(current_puck: Entity, field: Field, our_paddle: Entity) -> Vec | None:
    """Calculate the position to move to in order to intercept the puck.
    If we have more time than the puck to reach the shot line, we can wait. It returns None.
    If we don't have enough time or the puck is not moving we can use the defence algorith, it raises ValueError."""
    # Predict the puck's position and velocity at the shot line
    try:
        puck_pos, puck_v, puck_time_to_reach = predict_offence_pos_time(current_puck, field, 200)
    except ValueError:
        # If the puck is not moving in the x direction, we can't predict its position
        raise ValueError("Puck is not moving in the x direction, cannot predict position.")

    # Calculate the distance to the puck
    distance = (current_puck.pos - our_paddle.pos).abs()

    robot_time_to_reach = distance / ROBOT_SPEED

    if robot_time_to_reach < puck_time_to_reach - time_tolerance:
        # If the robot can reach the puck before it reaches the shot line, we can wait
        return None
    elif robot_time_to_reach > puck_time_to_reach + time_tolerance:
        # If the robot can't reach the puck before it reaches the shot line, we can use the defense strategy
        raise ValueError("Robot cannot reach puck in time.")
    else:
        # If the robot can reach the puck at the same time as it reaches the shot line, we can move to the puck's position
        return puck_pos
