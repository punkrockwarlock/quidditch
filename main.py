import pygame
import sys
from pygame.locals import *

# constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
MAP_WIDTH = 1000
MAP_HEIGHT = 1000
FPS = 60
STATUS = "TEST"

# initialise pygame and setup local variables
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

## classes
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.camera = Camera()

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.track = None

    def update(self):
        if self.track:
            self.x = self.track.x - (SCREEN_WIDTH / 2)          # update camera to keep tracked sprite in middle
            self.y = self.track.y - (SCREEN_HEIGHT / 2)

        if self.x < 0: self.x = 0
        if self.x > (MAP_WIDTH - SCREEN_WIDTH): self.x = MAP_WIDTH - SCREEN_WIDTH
        if self.y < 0: self.y = 0
        if self.y > (MAP_HEIGHT - SCREEN_HEIGHT): self.y = MAP_HEIGHT - SCREEN_HEIGHT

    def onScreen(self, sprite):
        return (sprite.x >= self.x and sprite.x <= (self.x + SCREEN_WIDTH)) and (sprite.y >= self.y and sprite.y <= (self.y + SCREEN_HEIGHT))

class TerrainBlock:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.image = pygame.image.load('./gfx/grass_block.png').convert()

    def draw(self):
        if self.game.camera.onScreen(self):
            local_x = self.x - self.game.camera.x
            local_y = self.y - self.game.camera.y
            self.game.screen.blit(self.image, Rect(local_x, local_y, self.image.get_width(), self.image.get_height()))

class TestPlayer:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.w = 10
        self.h = 10
        self.colour = Color(255, 0 , 0)

    def draw(self):
        if self.game.camera.onScreen(self):
            local_x = self.x - self.game.camera.x
            local_y = self.y - self.game.camera.y
            pygame.draw.rect(self.game.screen, self.colour, Rect(local_x, local_y, self.w, self.h))

## functions
def eventHandler():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            elif event.key == K_a:
                player2.x -= 10

            elif event.key == K_d:
                player2.x += 10

            elif event.key == K_w:
                player2.y -= 10

            elif event.key == K_s:
                player2.y += 10


game = Game()
player = TestPlayer(game, 100, 100)
player2 = TestPlayer(game, 800, 800)
ground = TerrainBlock(game, 950, 950)

game.camera.track = player2

while 1:
    # fill the screen with black
    game.screen.fill(Color(100, 100, 100))

    # limit game to FPS constant
    game.clock.tick(FPS)

    # check for user events
    eventHandler()

    # update the screen
    game.camera.update()
    player.draw()
    player2.draw()
    ground.draw()

    # display changes on screen
    pygame.display.flip()
