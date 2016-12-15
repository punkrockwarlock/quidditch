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

screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT), pygame.FULLSCREEN)

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
player_team.add(BasePlayer.Chaser(game, player_team.type))
player_team.add(BasePlayer.Chaser(game, player_team.type))
game.add_team(player_team)

opposition_team = classes.Team("player_controlled")
opposition_team.add(BasePlayer.Chaser(game, opposition_team.type))
opposition_team.add(BasePlayer.Chaser(game, opposition_team.type))
opposition_team.add(BasePlayer.Chaser(game, opposition_team.type))
game.add_team(opposition_team)

quaffle = Balls.Quaffle(game)
quaffle.position = Vec2d(200, 200)
game.quaffle = quaffle

game.add_goal(classes.Goal(game, Vec2d(100, 500)), "player_controlled")
game.add_goal(classes.Goal(game, Vec2d(100, 600)), "player_controlled")
game.add_goal(classes.Goal(game, Vec2d(100, 700)), "player_controlled")
game.add_goal(classes.Goal(game, Vec2d(4892, 500)), "ai_controlled")
game.add_goal(classes.Goal(game, Vec2d(4892, 600)), "ai_controlled")
game.add_goal(classes.Goal(game, Vec2d(4892, 700)), "ai_controlled")

game.camera.track = quaffle

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
    #print player.fsm.stateStack[len(player.fsm.stateStack) - 1]

    quaffle.update()
    #print functions.distance(player, player.goal[0])

    ground.draw()
    quaffle.draw()

    game.update_teams()
    game.draw_teams()
    game.draw_goals()

    # display changes on screen
    pygame.display.flip()
