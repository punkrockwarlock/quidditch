import pygame
import pygame.locals as local

import src.classes as classes
import src.functions as functions
import src.constants as const
from src.BasePlayer import BasePlayer


# initialise pygame and setup local variables
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))

# groups
game = classes.Game()

background = classes.Background(game)
ground = classes.Ground(game)

player = BasePlayer(game)
player.position.x = 200
player.controller = const.CONTROL_USER

player2 = BasePlayer(game)
game.all_players.add(player, player2)
# goal1 = Goal(game, 100, 300)

game.camera.track = player

while 1:
    # fill the screen with black
    game.screen.fill(local.Color(100, 100, 200))
    background.draw()

    # limit game to FPS constant
    game.clock.tick(const.FPS)

    # check for user events
    functions.eventHandler(player)

    # update the screen
    game.camera.update()
    player.update()
    player2.update()

    player.draw()
    player2.draw()
    ground.draw()

    # display changes on screen
    pygame.display.flip()
