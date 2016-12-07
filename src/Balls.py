import pygame
import SteeringManager
from Vector import Vec2d


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
        self.rect = pygame.Rect(self.position.x,
                                self.position.y,
                                self.image.get_width(),
                                self.image.get_height())

    def draw(self):
        if self.game.camera.onScreen(self):
            local_x = self.position.x - self.game.camera.x
            local_y = self.position.y - self.game.camera.y
            self.game.screen.blit(self.image,
                                  (local_x, local_y))


class Quaffle(Ball):
    def __init__(self, game):
        Ball.__init__(self, game)
        self.image = pygame.image.load("./gfx/quaffle.png")
        self.mask = pygame.mask.from_surface(self.image)
        self.held_by = None

    def update(self):
        self._update()
        if self.held_by:
            self.position = self.held_by.position
        else:
            self.position += self.velocity.normalized() * self.acceleration

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
        self.velocity = Vec2d(0, 0)
        self.velocity = self.velocity.rotated(angle)
        self.acceleration = power
        self.setPossession(None)
