import time
import threading

from GUI import App
from algo.algo import handle_new_vision_state
from algo.motor_interface import get_paddle_pos


def vision(app):
    """Placeholder for vision task"""
    for i in range(100000):
        time.sleep(0.010)
        app.log_queue.put(f"New frame {i}")
        if app.running:
            app.log_queue.put(f"Running step")
            handle_new_vision_state()
        else:
            app.log_queue.put(f"Not using frame")
        app.log_queue.put(str(get_paddle_pos()))
    app.log_queue.put("stopping")

app: App
if __name__ == '__main__':
    app = App()

    # Start the worker thread
    threading.Thread(target=vision, args=(app,), daemon=True).start()

    # TODO: start server for receiving motor state, callback: handle_new_motor_state()
    #  {just save it to variable that we can look at}
    # TODO: start camera feed, callback: handle_new_vision_state()
    # TODO: send "Ready" message each when camera is ready and motor is homed

    app.mainloop()
