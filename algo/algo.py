from algo.defensive import jitter_in_front_of_goal
from algo.model import Vec, Entity, Field
from algo.prediction import predict

LARGE_PUCK_RADIUS = 52 / 2
SMALL_PUCK_RADIUS = 50 / 2
PUCK_RADIUS = SMALL_PUCK_RADIUS
HUMAN_PADDLE_RADIUS = 67 / 2
ROBOT_PADDLE_RADIUS = 69 / 2 # half circle, assume fill circle for now

field = Field(w = 987, h = 494)
puck = Entity(Vec(0, 0), Vec(0, 0), SMALL_PUCK_RADIUS)
our_paddle = Entity(Vec(0, 0), Vec(0, 0), ROBOT_PADDLE_RADIUS)
opponent_paddle = Entity(Vec(0, 0), Vec(0, 0), HUMAN_PADDLE_RADIUS)

FULL_SPEED = Vec(0, 0)
def send_command(target_pos: Vec, target_v: Vec = None):
    if target_v is None:
        target_v = FULL_SPEED

    # TODO: use motor component
    ...

# get pos and velocity of our paddle
def get_our_paddle() -> (Vec, Vec):
    # TODO: use motor component
    ...

state = "start"

def run_step():
    # select strategy based on situation
    jitter_in_front_of_goal()

def handle_new_vision_state():
    # FEATURE: predict human action
    # set puck using vision, and maybe opponent_paddle

    run_step()

