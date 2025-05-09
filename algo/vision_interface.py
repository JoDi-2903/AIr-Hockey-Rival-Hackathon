import time

from algo.model import Vec
from puck_detection.puck_detection import get_and_use_frame

timestamp = 0.0
vision_puck_position: (float, float) = (0, 0)
vision_puck_velocity: (float, float) = (0, 0)

def vision_loop(app):
    """ Placeholder for vision task

    this runs in a separate thread for vision tasks and maybe polling
    """
    global vision_puck_position
    global vision_puck_velocity

    # FEATURE: see and predict human action

    while True:
        new_timestamp, pts = get_and_use_frame()
        app.log_queue.put(f"New frame")
        if app.running:
            dt = new_timestamp - timestamp
            last_pos = Vec(*(pts[1]))
            cur_pos = Vec(*(pts[0]))
            vision_puck_position = cur_pos
            vision_puck_velocity = (cur_pos - last_pos) / dt
        else:
            app.log_queue.put(f"Not using frame")
