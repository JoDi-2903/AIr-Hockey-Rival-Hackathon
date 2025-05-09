from algo.model import Vec
from coordinate_transform import field_to_machine_coordinates, machine_to_field_coordinates
from motor_control_system import MotorControlSystem

mcs: MotorControlSystem = MotorControlSystem()
mcs.connect()

def send_command(target_pos: Vec, velocity: float = 1.0):
    # print(f"current pos: {get_paddle_pos()}")
    # print(f"Sending command: {target_pos}")
    x, y = field_to_machine_coordinates((target_pos.x, target_pos.y))
    mcs.set_position(x, y, velocity)

def get_our_paddle() -> (Vec, Vec):
    """get pos and velocity of our paddle (should just read from var)"""
    raise NotImplementedError()

def get_paddle_pos() -> Vec:
    x, y = machine_to_field_coordinates(mcs.get_position)
    return Vec(x, y)
