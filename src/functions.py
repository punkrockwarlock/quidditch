import pygame
import math
import pygame.locals as local
import constants as const
from Vector import Vec2d
import sys


# functions
def eventHandler(game, player):
    keys = pygame.key.get_pressed()

    if keys[local.K_LEFT]:
        player.changeHeading("left")

    if keys[local.K_RIGHT]:
        player.changeHeading("right")

    if keys[local.K_UP]:
        player.changeHeading("up")

    if keys[local.K_DOWN]:
        player.changeHeading("down")

    if keys[local.K_s]:
        player.pass_quaffle()

    if keys[local.K_d]:
        player.player_tackle()

    for event in pygame.event.get():
        if event.type == local.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == local.KEYDOWN:
            if event.key == local.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == local.K_x:
                q = game.quaffle.getPossession()
                if q is not None:
                    print q.fsm.stateStack[len(q.fsm.stateStack) - 1]


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


# def distance(d_from, d_to):
#    return math.sqrt((d_to.x - d_from.x)**2 + (d_to.y - d_from.y)**2)


def get_closest(d_from, group):
    closest = Dummy(Vec2d(10000, 10000))
    for elem in group:
        if (distance(d_from.position, elem.position) < distance(d_from.position, closest.position)):
            closest = elem
    return closest

def pixel_collide(first, second):
    offset_x = (first.rect.left - second.rect.left)
    offset_y = (first.rect.top - second.rect.top)
    if (second.mask.overlap(first.mask, (offset_x, offset_y)) != None):
        return True
    else:
        return False

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

# chaser:
# self.team = ["team - me"]
# self.opposition = ["opposition"]
# self.team_chasers = ["chasers in team - me"]


def distance(from_sprite, to_sprite):
    return (to_sprite.position - from_sprite.position).get_length()


def groupClosest(group, sprite):
    closest = None
    for member in group:
        if closest is not None:
            if (distance(member, sprite) < distance(closest, sprite)):
                closest = member
        else:
            closest = member

    return closest


def groupPossession(game, group):
    return group.has(game.balls["quaffle"].held_by)


def groupIsBlocking(group, from_sprite, to_sprite):
    blocked = False
    for member in group:
        member_centre = Vec2d(member.pos.x + member.rect.get_width() / 2,
                              member.pos.y + member.rect.get_height() / 2)
        radius = member.rect.get_width() / 2
        closest_point = closest_point_on_seg(from_sprite.position,
                                             to_sprite.position,
                                             member_centre)
        if distance(member_centre, closest_point) < radius:
                blocked = True
    return blocked


def closest_point_on_seg(seg_a, seg_b, circ_pos):
    seg_v = seg_b - seg_a
    pt_v = circ_pos - seg_a
    if seg_v.len() <= 0:
        raise ValueError, "Invalid segment length"
    seg_v_unit = seg_v / seg_v.get_length()
    proj = pt_v.dot(seg_v_unit)
    if proj <= 0:
        return seg_a.copy()
    if proj >= seg_v.get_length():
        return seg_b.copy()
    proj_v = seg_v_unit * proj
    closest = proj_v + seg_a
    return closest
