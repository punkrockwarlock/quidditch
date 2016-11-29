# constants

# system controls
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
MAP_WIDTH = 9984
MAP_HEIGHT = 2024
FPS = 60
STATUS = "TEST"

# used to control ground creation
GRND_BLOCK_W = 64
GRND_BLOCK_H = 64
GROUND_DEPTH = 1
GROUND_LEVEL = MAP_HEIGHT - GRND_BLOCK_H

# used to control if baseplayer object is controlled by user or AI
CONTROL_USER = 1
CONTROL_AI = 2

# used in chaser_fsm
GRAB_DISTANCE = 20
PRESSURE_DISTANCE = 50
MAX_PASS_DIST = 500
MAX_SHOOT_DIST = 500
CHASER_AVOID = 300
