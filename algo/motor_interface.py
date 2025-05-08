from algo.model import Vec

FULL_SPEED = Vec(0, 0)
def send_command(target_pos: Vec, target_v: Vec = None):
    if target_v is None:
        target_v = FULL_SPEED

    # TODO: use motor component
    ...

def get_our_paddle() -> (Vec, Vec):
    """get pos and velocity of our paddle (should just read from var)"""
    # TODO: use motor component
    return (Vec(), Vec())
