import time
import threading

from GUI import App
from algo.algo import handle_new_vision_state


def vision(app):
    """Placeholder for vision task"""
    for i in range(10):
        time.sleep(1)
        app.log_queue.put(f"New frame {i}")
        if app.running:
            app.log_queue.put(f"Running step")
            handle_new_vision_state()
        else:
            app.log_queue.put(f"Not using frame")


if __name__ == '__main__':
    app = App()

    # Start the worker thread
    threading.Thread(target=vision, args=(app,), daemon=True).start()

    # TODO: start server for receiving motor state, callback: handle_new_motor_state()
    #  {just save it to variable that we can look at}
    # TODO: start camera feed, callback: handle_new_vision_state()
    # TODO: send "Ready" message each when camera is ready and motor is homed

    app.mainloop()
