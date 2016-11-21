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

        self.player_team = pygame.sprite.Group()
        self.opposition_team = pygame.sprite.Group()
        self.all_players = pygame.sprite.Group()

        self.teams = {}

    def add_team(self, team):
        if team.type in ("player_controlled", "ai_controlled"):
            if team_type not in self.teams:
                self.teams[team_type] = team
            else:
                raise KeyError("That team already exists")
        else:
            raise ValueError("Invalid team type")

    def get_team(self, type_or_player):
        if type_or_player in ("player_controlled", "ai_controlled"):
            return self.teams[type_or_player]
        else:
            for team in self.teams.values():
                if player in team:
                    return team


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.track = None

    def onScreen(self, sprite):
        top_left = (sprite.position.x >= self.x and
                  sprite.position.x <= (self.x + const.SCREEN_WIDTH)) and (
                (sprite.position.y >= self.y and
                 sprite.position.y <= (self.y + const.SCREEN_HEIGHT)))
        top_right = (sprite.position.x + sprite.image.get_width() >= self.x and
                  sprite.position.x + sprite.image.get_width() <= (self.x + const.SCREEN_WIDTH)) and (
                (sprite.position.y >= self.y and
                 sprite.position.y <= (self.y + const.SCREEN_HEIGHT)))
        return top_left or top_right

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
                self.y = const.MAP_HEIGHT - const.SCREEN_HEIGHT


class Background:
    def __init__(self, game):
        self.game = game
        self.main_image = pygame.image.load("./gfx/bg.png").convert_alpha()
        self.make()

    def make(self):
        image = pygame.Surface([const.MAP_WIDTH, const.MAP_HEIGHT])
        image.fill(local.Color(192, 239, 247))
        image.blit(self.main_image,
                   (0, const.MAP_HEIGHT - self.main_image.get_height()))
        self.main_image = image

    def draw(self
        drawRect = local.Rect(self.game.camera.x,
                              self.game.camera.y,
                              const.SCREEN_WIDTH,
                              const.SCREEN_HEIGHT)

        self.image = self.main_image.subsurface(drawRect)
        self.game.screen.blit(self.image, (0, 0))


class Ground:
    def __init__(self, game):
        self.game = game
        self.blocks = []
        self.build()

    def build(self):
        for x in range(0, const.MAP_WIDTH, const.GRND_BLOCK_W):
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
        self.image = pygame.image.load("./gfx/grass.png").convert()

    def draw(self):
        local_x = self.position.x - self.game.camera.x
        local_y = self.position.y - self.game.camera.y
        if self.game.camera.onScreen(self):
            self.game.screen.blit(self.image, (local_x, local_y))

class Team(pygame.sprite.Group):
    def __init__(self, team_type):
        pygame.sprite.Group.__init__()
        self.type = team_type

    def _findPlayer(self, position):
        for player in self:
            if player.type == position:
                return player
        return None

    def get_player(self, position):
        if position in ("keeper", "seeker"):
            return self._findPlayer(position)
        else:
            raise KeyError("Could not find the position in team")

    def get_group(self, group_name):
        theGroup = pygame.sprite.Group()
        if group_name in ("chaser", "beater"):
            for player in self:
                if player.type == group_name:
                    theGroup.add(v)
        return theGroup
