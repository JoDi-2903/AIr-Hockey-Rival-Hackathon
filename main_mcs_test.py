from motor_control_system import MotorControlSystem
import time

mcs = MotorControlSystem()
mcs.connect()
mcs.set_position(x=120, y=100, velocity=1, acceleration=1)
print(f"Current position: {mcs.get_position()}, current velocity: {mcs.get_velocity()}")
time.sleep(5)
print(f"Current position: {mcs.get_position()}, current velocity: {mcs.get_velocity()}")
mcs.set_position(x=100, y=100, velocity=1, acceleration=1)
time.sleep(1)
print(f"Current position: {mcs.get_position()}, current velocity: {mcs.get_velocity()}")
mcs.close()
