from algo.constants import PUCK_RADIUS, field
from algo.model import Vec
from algo.motor_interface import send_command, get_paddle_pos
from algo.util import clamp

state = "start"
def jitter_in_front_of_goal():
    global state
    global field
    bottom = field.h / 2 - field.home_goal_height / 2
    top = field.h / 2 + field.home_goal_height / 2
    target_x = PUCK_RADIUS

    pad = get_paddle_pos()

    eps = 30 # what distance to turn around at

    match state:
        case "down":
            # wait until we are at our goal
            if (pad.is_close_to(Vec(target_x, bottom), eps)):
                send_command(Vec(target_x, top))
                state = "up"
        case "up":
            if (pad.is_close_to(Vec(target_x, top), eps)):
                send_command(Vec(target_x, bottom))
                state = "down"
        case _:
            send_command(Vec(target_x, bottom))
            state = "down"


def mimic_puck_y():
    global state
    global puck
    global field

    bottom = field.h / 2 - field.home_goal_height / 2
    top = field.h / 2 + field.home_goal_height / 2

    target_y = clamp(puck.pos.y, bottom, top)
    target_x = PUCK_RADIUS / 2
    target = Vec(target_x, target_y)

    if not puck.pos.is_close_to(target):
        send_command(target)
