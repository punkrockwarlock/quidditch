import pygame
import pygame.locals as local

import src.classes as classes
import src.functions as functions
import src.constants as const
import src.BasePlayer as BasePlayer
import src.Balls as Balls
from src.Vector import Vec2d


# initialise pygame and setup local variables
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))

# groups
game = classes.Game()

background = classes.Background(game)
ground = classes.Ground(game)

player = BasePlayer.Chaser(game, "ai_controlled")
player.position.x = 200
player3 = BasePlayer.Chaser(game, "ai_controlled")
player3.position.x = 400

player_team = classes.Team("ai_controlled")
player_team.add(player)
player_team.add(player3)
game.add_team(player_team)

player2 = BasePlayer.Chaser(game, "player_controlled")
quaffle = Balls.Quaffle(game)

opposition_team = classes.Team("player_controlled")
opposition_team.add(player2)
game.add_team(opposition_team)

quaffle.position = Vec2d(200, 200)
game.all_players.add(player, player2)
game.quaffle = quaffle
game.quaffle.setPossession(player2)
game.add_goal(classes.Goal(game), "player_controlled")

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
    print player.fsm.stateStack[len(player.fsm.stateStack) - 1]
    player2._update()
    player3.update()
    quaffle.update()
    #print functions.distance(player, player.goal[0])

    ground.draw()
    quaffle.draw()

    #game.update_teams()
    game.draw_teams()
    game.draw_goals()

    # display changes on screen
    pygame.display.flip()
