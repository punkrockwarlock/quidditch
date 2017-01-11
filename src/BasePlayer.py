import pygame
import pygame.locals as local
import SteeringManager
import functions
import constants as const
import math
import classes
import FSM
import random
from Vector import Vec2d


class BasePlayer(pygame.sprite.Sprite):
    def __init__(self, game, team):
        pygame.sprite.Sprite.__init__(self)
        self.steerMngr = SteeringManager.SteeringManager(game, self)

        self.game = game
        self.team = team
        self.type = None
        self.opposition = "player_controlled" if team == "ai_controlled" else "ai_controlled"
        self.position = Vec2d(100, 100)
        self.velocity = Vec2d(0, 0)
        self.new_velocity = Vec2d(0, 0)
        self.acceleration = 0
        self.ai_acceleration = 2

        # determines if this is controlled by user or AI
        self.controller = const.CONTROL_AI

        # start_image as a starting point for rotation
        if self.team == "player_controlled":
            self.start_image = pygame.image.load("./gfx/player.png").convert_alpha()
        else:
            self.start_image = pygame.image.load("./gfx/opposition.png").convert_alpha()
        self.image = self.start_image
        self.rect = local.Rect(self.position.x,
                               self.position.y,
                               self.image.get_width(),
                               self.image.get_height())
        self.mask = pygame.mask.from_surface(self.image)

        # used to show which way self.image is pointing
        self.pointing = -1

        self.max_see_ahead = 50
        self.max_avoid_force = 5

        # should be overwritten by inherited classes
        self.max_force = 5
        self.max_velocity = 10
        self.mass = 5
        self.speed = 0

        self.drawBounds = False

    def changeHeading(self, direction):
        if self.controller == const.CONTROL_AI:
            return

        if direction == "left":
            vec = Vec2d(-0.1, 0)
        elif direction == "right":
            vec = Vec2d(0.1, 0)
        elif direction == "up":
            vec = Vec2d(0, -0.1)
        elif direction == "down":
            vec = Vec2d(0, 0.1)
        self.acceleration += 0.4

        if self.acceleration > self.max_speed:
            self.acceleration = self.max_speed
        elif self.acceleration < 0:
            self.acceleration = 0

        if (vec.x < 0 and self.pointing == 1):
            self.acceleration -= 0.2
            if self.acceleration <= 0:
                self.velocity.x *= -1
        elif (vec.x > 0 and self.pointing == -1):
            self.acceleration -= 0.2
            if self.acceleration <= 0:
                self.velocity.x *= -1

        self.velocity += vec
        self.velocity = self.velocity.normalized()

    def rotateToHeading(self):
        if self.velocity.x >= 0:
            self.pointing = 1
        else:
            self.pointing = -1

        angle = self.velocity.get_angle()
        if self.pointing == 1:
            temp_image = pygame.transform.flip(self.start_image, 1, 0)
            angle *= -1
            temp_image = pygame.transform.rotate(temp_image, angle)
        else:
            temp_image = self.start_image
            if (angle < 180):
                angle = 180 - angle
                temp_image = pygame.transform.rotate(temp_image, angle)

        self.image = temp_image
        self.mask = pygame.mask.from_surface(self.image)

    def _update(self):
        self.rotateToHeading()
        self.checkCollisions()

        # this will run if controlled by AI
        if self.controller == const.CONTROL_AI:
            self.steerMngr.update()
            if self.acceleration > 0:
                self.acceleration = self.acceleration - const.DAMPING
            elif self.acceleration < 0:
                self.acceleration = 0

        if self.controller == const.CONTROL_USER:
            self.position += functions.truncate((self.velocity.normalized() *
                                                self.acceleration),
                                                self.max_speed)

        local_x = self.position.x - self.game.camera.x
        local_y = self.position.y - self.game.camera.y
        self.rect = local.Rect(local_x,
                               local_y,
                               self.image.get_width(),
                               self.image.get_height())
        self.drawBounds = False

    def _inBounds(self):
        # if x position is more than 0
        if (self.position.x <= 0):
            self.position.x = 3
            self.reset()
        if (self.position.x + self.start_image.get_width() > (const.MAP_WIDTH)):
            self.position.x = const.MAP_WIDTH - self.start_image.get_width() - 3
            self.reset()
        if (self.position.y <= 0):
            self.position.y = 3
            self.reset()
        if (self.position.y + self.start_image.get_height() >= (const.MAP_HEIGHT - const.GRND_BLOCK_H)):
            self.position.y = const.MAP_HEIGHT - const.GRND_BLOCK_H - self.start_image.get_height() - 3
            self.reset()

    def _playerCollisions(self):
        temp_group = self.game.all_players.copy()
        temp_group.remove(self)
        collided_with = pygame.sprite.spritecollideany(self, temp_group)
        temp_group.empty()
        temp_group = None
        if collided_with:
            if functions.pixel_collide(collided_with, self):
                return collided_with

    def checkCollisions(self):
        self._inBounds()
        player_collided = self._playerCollisions()
        if player_collided:
            #self.reset()
            #self.velocity = (player_collided.position - self.position) * -1
            self.acceleration = 2

    def reset(self):
        ''' resets velocity and acceleration to 0 '''
        self.velocity *= -1
        self.acceleration = 0

    def draw(self):
        if self.game.camera.onScreen(self):
            local_x = self.position.x - self.game.camera.x
            local_y = self.position.y - self.game.camera.y
            self.game.screen.blit(self.image,
                                  (local_x, local_y))
            if self.drawBounds:
                pygame.draw.rect(self.game.screen, (255, 0, 0), self.rect, 1)


class Chaser(BasePlayer):
    def __init__(self, game, team):
        BasePlayer.__init__(self, game, team)
        self.type = "chaser"
        self.fsm = FSM.fsm_Chaser(self)
        self.acceleration = 0.01

        # personalised
        self.shoot_distance = 500
        self.shoot_power = 30

        self.skill_attack = 5
        self.skill_defend = 8

        self.max_speed = self.max_velocity + math.floor(random.random() * 5)

    def getShootDist(self):
        return self.shoot_distance

    def update(self):
        self._update()

        if self.controller == const.CONTROL_AI:
            if self.speed < self.max_speed:
                self.speed += self.acceleration
            else:
                self.speed = self.max_speed
            self.fsm.update()

        if self.controller == const.CONTROL_USER:
            self.checkQuaffle()

    def checkQuaffle(self):
        if self.game.quaffle.getPossession() is None:
            if functions.pixel_collide(self.game.quaffle, self):
                self.game.quaffle.setPossession(self)

    def shoot(self):
        oppGoal = self.game.get_goal(self)
        vec_between = (oppGoal.position - self.position).normalized()
        self.game.quaffle.throw(vec_between, self.shoot_power)

    def pass_to(self, other):
        vec_between = (other.position - self.position).normalized()
        self.game.quaffle.throw(vec_between, self.shoot_power)

    def pass_quaffle(self):
        if self.pointing == 1:
            self.game.quaffle.position.x = self.position.x + self.start_image.get_width()
        self.game.quaffle.throw(self.velocity, self.shoot_power)

    def player_tackle(self):
        if functions.distance(self.game.quaffle, self) < const.TACKLE_DIST:
            self.game.quaffle.setPossession(self)

    def tackle(self, oppChaser):
        tackle_chance = math.floor((self.skill_attack + random.random() * 4))
        if tackle_chance > oppChaser.skill_defend:
            return True
        else:
            return False
