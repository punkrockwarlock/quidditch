import pygame
import math
import pygame.locals as local
import src.constants as const
from src.Vector import Vec2d
import sys


# functions
def eventHandler(player):
    keys = pygame.key.get_pressed()

    if keys[local.K_a]:
        player.changeHeading("left")

    if keys[local.K_d]:
        player.changeHeading("right")

    if keys[local.K_w]:
        player.changeHeading("up")

    if keys[local.K_s]:
        player.changeHeading("down")

    for event in pygame.event.get():
        if event.type == local.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == local.KEYDOWN:
            if event.key == local.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == local.K_x:
                print player.position


def onMap(sprite):
    bool_x = (sprite.position.x >= 0 and sprite.position.x + sprite.image.get_width() <= (const.MAP_WIDTH))
    bool_y = (sprite.position.y >= 0 and sprite.position.y + sprite.image.get_height() <= (const.MAP_HEIGHT - const.GRND_BLOCK_H))


def point_direction(x, y, t_x, t_y):
    return math.atan2(t_y-y, t_x-x) * 180/math.pi


def vec_point_direction(vec1, vec2):
    return math.atan2(vec2.y - vec1.y, vec2.x - vec1.x) * 180/math.pi


def lineIntersectsCircle(ahead, ahead2, obstacle):
    return distance(obstacle.pos, ahead) <= PL_INFLUENCE or distance(obstacle.pos, ahead2) <= PL_INFLUENCE


def sign(num):
    if (num <= 0):
        return -1
    elif (num > 0):
        return 1


def distance(d_from, d_to):
    return math.sqrt((d_to.x - d_from.x)**2 + (d_to.y - d_from.y)**2)


def get_closest(d_from, group):
    closest = Dummy(Vec2d(10000, 10000))
    for elem in group:
        if (distance(d_from.position, elem.position) < distance(d_from.position, closest.position)):
            closest = elem
    return closest


def circle_collide(first, second):
    between = distance(first, second)
    rad1 = (first.rect.width + first.rect.height) / 2
    rad2 = (first.rect.width + first.rect.height) / 2
    if (between <= (rad1 + rad2)):
        return True


def influence_collide(first, second):
    between = distance(first, second)
    influence = 100
    if (between <= (rad * 2)):
        return True


def collide_player(d_from):
    players = []
    for elem in object_list:
        if elem.type == 'player':
            players.append(elem)
    for player in players:
        if (circle_collide(d_from, player)):
            return player
    return None


def truncate(vector, m):
    magnitude = vector.length
    if (magnitude > m):
        vector *= m / magnitude
    return vector


class Dummy:
    def __init__(self, vec):
        self.position = vec
