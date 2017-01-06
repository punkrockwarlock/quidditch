# constants

# system controls
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768
MAP_WIDTH = 6992
MAP_HEIGHT = 2024
FPS = 40
STATUS = "TEST"

# environment constants
GRAVITY = 0.8

# used to control ground creation
GRND_BLOCK_W = 64
GRND_BLOCK_H = 64
GROUND_DEPTH = 1
GROUND_LEVEL = MAP_HEIGHT - GRND_BLOCK_H

# used to control if baseplayer object is controlled by user or AI
CONTROL_USER = 1
CONTROL_AI = 2

# used in steering manager
SEPARATION_DIST = 300

# used in chaser_fsm
DAMPING = 0.3
GRAB_DISTANCE = 101
PRESSURE_DISTANCE = 80
MAX_PASS_DIST = 600
MIN_PASS_DIST = 200
SUPPORT_DIST = MAX_PASS_DIST - 100
MAX_SHOOT_DIST = 500
CHASER_AVOID = 300
POST_SHOOT_DIST = 100
TACKLE_DIST = 60
DEF_IN_FRONT = 50
