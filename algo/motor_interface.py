from algo.model import Vec
from motor_control_system import MotorControlSystem

mcs = MotorControlSystem()
mcs.connect()

# TODO: ACS -> MCS translation goes in here

FULL_SPEED = Vec(0, 0)
def send_command(target_pos: Vec, velocity: float = 1.0):
    # print(f"current pos: {get_paddle_pos()}")
    # print(f"Sending command: {target_pos}")
    mcs.set_position(target_pos.x, target_pos.y, velocity)

def get_our_paddle() -> (Vec, Vec):
    """get pos and velocity of our paddle (should just read from var)"""
    raise NotImplementedError()

def get_paddle_pos() -> Vec:
    x, y = mcs.get_position
    return Vec(x, y)
