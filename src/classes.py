import pygame
import pygame.locals as local
import constants as const
from Vector import Vec2d


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((const.SCREEN_WIDTH,
                                               const.SCREEN_HEIGHT))
        self.camera = Camera()
        self.clock = pygame.time.Clock()
        self.fps = 60


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.track = None

    def onScreen(self, sprite):
        return (sprite.position.x >= self.x and
                sprite.position.x <= (self.x + const.SCREEN_WIDTH)) and (
                (sprite.position.y >= self.y and
                 sprite.position.y <= (self.y + const.SCREEN_HEIGHT)))

    def update(self):
        if self.track:
            self.x = self.track.position.x - const.SCREEN_WIDTH / 2
            self.y = self.track.position.y - const.SCREEN_HEIGHT / 2

            if self.x < 0:
                self.x = 0
            elif (self.x + const.SCREEN_WIDTH) > const.MAP_WIDTH:
                self.x = const.MAP_WIDTH - const.SCREEN_WIDTH
            if self.y < 0:
                self.y = 0
            elif (self.y + const.SCREEN_HEIGHT) > const.MAP_HEIGHT:
                self.y = const.MAP_WIDTH - const.SCREEN_WIDTH

#class Background:


class Ground:
    def __init__(self, game):
        self.game = game
        self.blocks = []
        self.build()

    def build(self):
        for x in range(0, const.SCREEN_WIDTH, const.GRND_BLOCK_W):
            self.blocks.append(GroundBlock(self.game,
                               Vec2d(x,
                                     const.MAP_HEIGHT - const.GRND_BLOCK_H)))

    def draw(self):
        for block in self.blocks:
            block.draw()


class GroundBlock:
    def __init__(self, game, pos):
        self.game = game
        self.position = pos
        self.image = pygame.image.load("./gfx/grass.png")

    def draw(self):
        if self.game.camera.onScreen(self):
            self.game.screen.blit(self.position, self.image)
