import time

vision_puck_position: (float, float)

def vision_loop(app):
    """ Placeholder for vision task

    this runs in a separate thread for vision tasks and maybe polling
    """
    global vision_puck_position

    # FEATURE: predict human action
    # TODO: set puck using vision, and maybe opponent_paddle


    for i in range(100000):
        time.sleep(0.033)
        app.log_queue.put(f"New frame {i}")
        if app.running:
            app.log_queue.put(f"Running step")
            vision_puck_position = (0, 0)
        else:
            app.log_queue.put(f"Not using frame")
    app.log_queue.put("stopping")