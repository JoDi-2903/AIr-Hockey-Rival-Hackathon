from algo.constants import SMALL_PUCK_RADIUS, HUMAN_PADDLE_RADIUS, ROBOT_PADDLE_RADIUS
from algo.defensive import jitter_in_front_of_goal
from algo.model import Vec, Entity

puck = Entity(Vec(0, 0), Vec(0, 0), SMALL_PUCK_RADIUS)
our_paddle = Entity(Vec(0, 0), Vec(0, 0), ROBOT_PADDLE_RADIUS)
opponent_paddle = Entity(Vec(0, 0), Vec(0, 0), HUMAN_PADDLE_RADIUS)



def run_step():
    # select strategy based on situation
    jitter_in_front_of_goal()


def handle_new_vision_state():
    # FEATURE: predict human action
    # set puck using vision, and maybe opponent_paddle

    run_step()
