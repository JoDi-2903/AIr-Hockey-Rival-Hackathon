from algo.constants import SMALL_PUCK_RADIUS, HUMAN_PADDLE_RADIUS, ROBOT_PADDLE_RADIUS
from algo.defensive import jitter_in_front_of_goal
from algo.model import Vec, Entity
from algo.motor_interface import get_paddle_pos
from algo.vision_interface import vision_puck_position

puck = Entity(Vec(0, 0), Vec(0, 0), SMALL_PUCK_RADIUS)
our_paddle = Entity(Vec(0, 0), Vec(0, 0), ROBOT_PADDLE_RADIUS)
opponent_paddle = Entity(Vec(0, 0), Vec(0, 0), HUMAN_PADDLE_RADIUS)

def run_step():
    # fetch current data
    puck.pos = Vec(*vision_puck_position)
    # opponent_paddle.pos = Vec(*vision_opponent_position)
    our_paddle.pos = get_paddle_pos()

    # select strategy based on situation
    if True:
        jitter_in_front_of_goal()
