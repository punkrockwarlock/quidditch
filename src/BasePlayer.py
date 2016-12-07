import pygame
import pygame.locals as local
import SteeringManager
import functions
import constants as const
import classes
import FSM
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
        self.start_image = pygame.image.load("./gfx/player.png").convert_alpha()
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
        self.max_velocity = 20
        self.mass = 5

    def changeHeading(self, direction):
        if self.controller == const.CONTROL_AI:
            return

        if direction == "left":
            vec = Vec2d(-1, 0)
            self.acceleration += 0.4
        elif direction == "right":
            vec = Vec2d(1, 0)
            self.acceleration += 0.4
        elif direction == "up":
            vec = Vec2d(0, -1)
            self.acceleration += 0.1
        elif direction == "down":
            vec = Vec2d(0, 1)
            self.acceleration += 0.2

        if (vec.x < 0 and self.pointing == 1):
            if self.acceleration > 0:
                self.acceleration = self.acceleration - 0.4
            elif self.acceleration < 0:
                self.acceleration = 0
        elif (vec.x > 0 and self.pointing == -1):
            if self.acceleration > 0:
                self.acceleration = self.acceleration - 0.4
            elif self.acceleration < 0:
                self.acceleration = 0

        self.velocity += vec

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

        if self.controller == const.CONTROL_USER:
            pass
            #self.position += functions.truncate((self.velocity.normalized() *
                                                #self.acceleration),
                                                #self.max_velocity)

        # slow down acceleration and make sure it isn't < 0
        if self.acceleration > 0:
            self.acceleration = self.acceleration - 0.1
        elif self.acceleration < 0:
            self.acceleration = 0

        self.rect = local.Rect(self.position.x,
                               self.position.y,
                               self.image.get_width(),
                               self.image.get_height())

    def _inBounds(self):
        # if x position is more than 0
        if (self.position.x <= 0):
            self.position.x = 1
            self.reset()
        if (self.position.x + self.start_image.get_width() >= (const.MAP_WIDTH)):
            self.position.x = const.MAP_WIDTH - self.start_image.get_width() - 1
            self.reset()
        if (self.position.y <= 0):
            self.position.y = 1
            self.reset()
        if (self.position.y + self.start_image.get_height() >= (const.MAP_HEIGHT - const.GRND_BLOCK_H)):
            self.position.y = const.MAP_HEIGHT - const.GRND_BLOCK_H - self.start_image.get_height() - 1
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
            self.reset()
            self.velocity = (player_collided.position - self.position) * -1
            self.acceleration = 2

    def reset(self):
        ''' resets velocity and acceleration to 0 '''
        self.velocity = Vec2d(0, 0)
        self.acceleration = 0

    def draw(self):
        if self.game.camera.onScreen(self):
            local_x = self.position.x - self.game.camera.x
            local_y = self.position.y - self.game.camera.y
            self.game.screen.blit(self.image,
                                  (local_x, local_y))


class Chaser(BasePlayer):
    def __init__(self, game, team):
        BasePlayer.__init__(self, game, team)
        self.type = "chaser"
        self.fsm = FSM.fsm_Chaser(self)
        self.goal = []

        # personalised
        self.shoot_distance = 100
        self.shoot_power = 20

    def getShootDist(self):
        return self.shoot_distance

    def update(self):
        self._update()

        if self.controller == const.CONTROL_AI:
            self.fsm.update()

    def shoot(self):
        angle_to_goal = self.position.get_angle_between(self.goal[0].position)
        self.game.quaffle.throw(angle_to_goal, self.shoot_power)
