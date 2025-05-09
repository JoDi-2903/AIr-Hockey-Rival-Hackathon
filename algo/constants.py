from algo.model import Field

LARGE_PUCK_RADIUS = 52 / 2
SMALL_PUCK_RADIUS = 50 / 2
PUCK_RADIUS = SMALL_PUCK_RADIUS
HUMAN_PADDLE_RADIUS = 67 / 2
ROBOT_PADDLE_RADIUS = 69 / 2 # half circle, assume fill circle for now
field = Field(w = 987, h = 494, home_goal_height=186, opponent_goal_height=189)
BASE_X = 62
