import time
import threading

from GUI import App
from algo.algo import run_step
from algo.vision_interface import vision_loop
from algo.motor_interface import mcs
from motor_control_system import MotorControlSystem

dt = .01

def game_loop(app):
    while True:
        before = time.time()
        if app.running:
            run_step()
        after = time.time()
        time.sleep(max(.0, dt - (after-before))) # 100Hz

if __name__ == '__main__':
    app = App()

    threading.Thread(target=game_loop, args=(app,), daemon=True).start()
    threading.Thread(target=vision_loop, args=(app,), daemon=True).start()
    # global mcs
    # mcs = MotorControlSystem(app)

    app.mainloop()
