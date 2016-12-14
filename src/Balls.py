import pygame
import SteeringManager
from Vector import Vec2d
import constants as const


class Ball(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.steerMngr = SteeringManager.SteeringManager(game, self)
        self.game = game
        self.position = Vec2d(0, 0)
        self.velocity = Vec2d(0, 0)
        self.acceleration = 0

        self.image = None
        self.rect = pygame.Rect(self.position.x,
                                self.position.y,
                                0, 0)

    def _update(self):
        self._inBounds()
        self.rect = pygame.Rect(self.position.x,
                                self.position.y,
                                self.image.get_width(),
                                self.image.get_height())

    def _inBounds(self):
        # if x position is more than 0
        if (self.position.x <= 0):
            self.position.x = 1
            self.reset()
        if (self.position.x + self.image.get_width() >= (const.MAP_WIDTH)):
            self.position.x = const.MAP_WIDTH - self.image.get_width() - 1
            self.reset()
        if (self.position.y <= 0):
            self.position.y = 1
            self.reset()
        if (self.position.y + self.image.get_height() >= (const.MAP_HEIGHT - const.GRND_BLOCK_H)):
            self.position.y = const.MAP_HEIGHT - const.GRND_BLOCK_H - self.image.get_height() - 1
            self.reset()

    def draw(self):
        if self.game.camera.onScreen(self):
            local_x = self.position.x - self.game.camera.x
            local_y = self.position.y - self.game.camera.y
            self.game.screen.blit(self.image,
                                  (local_x, local_y))

    def reset(self):
        ''' resets velocity and acceleration to 0 '''
        self.velocity = Vec2d(0, 0)
        self.acceleration = 0


class Quaffle(Ball):
    def __init__(self, game):
        Ball.__init__(self, game)
        self.image = pygame.image.load("./gfx/quaffle.png")
        self.mask = pygame.mask.from_surface(self.image)
        self.held_by = None

    def update(self):
        self._update()
        if self.held_by:
            self.position = self.held_by.position.copy()
        else:
            self.position += self.velocity.normalized() * self.acceleration

        if self.acceleration > 0:
            self.acceleration = self.acceleration - const.DAMPING
        elif self.acceleration < 0:
            self.acceleration = 0

        gravity_vec = Vec2d(0, const.GRAVITY).normalized()
        self.velocity += gravity_vec * 0.01

    def draw(self):
        if self.game.camera.onScreen(self):
            local_x = self.position.x - self.game.camera.x
            local_y = self.position.y - self.game.camera.y
            self.game.screen.blit(self.image,
                                  (local_x, local_y))

    def setPossession(self, player):
        self.held_by = player

    def getPossession(self):
        return self.held_by

    def throw(self, angle, power):
        self.velocity = angle
        self.acceleration = power
        self.setPossession(None)
