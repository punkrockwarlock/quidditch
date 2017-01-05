from Vector import Vec2d
import functions
import random
import constants as const


class SteeringManager:
    def __init__(self, game, host):
        self.game = game
        self.host = host
        self.steering = Vec2d(0, 0)

        self.wanderAngle = 0

    def collisionAvoidance(self):
        ahead = self.host.position + (self.host.velocity.normalized() *
                                      self.host.max_see_ahead)
        # ahead2 = self.host.position + ((self.host.velocity.normalized() *
                                        # self.host.max_see_ahead) * 0.5)

        mostThreatening = functions.groupClosest(self.game.get_team(self.host.opposition),
                                                 self.host)

        if (functions.distance(self.host, mostThreatening) > 100):
            mostThreatening = None
        avoidance = Vec2d(0, 0)
        if (mostThreatening is not None):
            avoidance = ahead - mostThreatening.position
            avoidance = avoidance.normalized()
            avoidance *= self.host.max_force
        self.steering += avoidance

    def separation(self):
        v = Vec2d(0, 0)
        neighborCount = 0

        for agent in self.game.get_team(self.host):
            if (functions.distance(agent, self.host) < const.SEPARATION_DIST):
                v.x += agent.position.x - self.host.position.x
                v.y += agent.position.y - self.host.position.y
                neighborCount += 1

        v.x /= neighborCount
        v.y /= neighborCount
        v = Vec2d(v.x - self.host.position.x, v.y - self.host.position.y)
        v = v.normalized()
        v *= -1
        return v

    def seek(self, target, slowingRadius=1):
        self.steering += self.doSeek(target, slowingRadius)

    def flee(self, target):
        self.steering += self.doFlee(target)

    def wander(self):
        self.steering += self.doWander()

    def evade(self, target):
        self.steering += self.doEvade(target)

    def pursuit(self, target):
        self.steering += self.doPursuit(target)

    def update(self):
        sep = self.separation() * 5
        velocity = self.host.velocity

        self.steering += sep
        self.steering = functions.truncate(self.steering, self.host.max_force)
        self.steering = self.steering / self.host.mass

        # velocity += self.steering
        velocity = functions.truncate(velocity + self.steering, self.host.speed)

        self.host.velocity = velocity
        self.host.position += velocity

    def reset(self):
        self.steering = Vec2d(0, 0)

    def doSeek(self, target, slowingRadius=0):
        desired = target - self.host.position

        distance = desired.get_length()

        if (distance <= slowingRadius):
            desired = desired.normalized() * self.host.max_speed * (distance / slowingRadius)
        else:
            desired = desired.normalized() * self.host.max_speed

        force = desired - self.host.velocity

        return force

    def doFlee(self, target):
        desired = (self.host.position - target)
        desired = desired.normalized() * self.host.max_velocity
        force = desired - self.host.velocity

        return force

    def doWander(self):
        circleCentre = Vec2d(self.host.velocity)
        circleCentre = circleCentre.normalized()
        circleCentre *= self.game.CIRCLE_DISTANCE

        displacement = Vec2d(0, -1)
        displacement *= self.game.CIRCLE_RADIUS

        displacement.angle = self.wanderAngle

        self.wanderAngle += (random.random() * self.game.ANGLE_CHANGE) - (self.game.ANGLE_CHANGE * .5)
        wanderForce = circleCentre + displacement
        return wanderForce

    def doEvade(self, target):
        distance = target - self.host.position
        updatesAhead = distance.get_length() / self.host.max_velocity
        futurePosition = target.position + target.velocity * updatesAhead
        return self.doFlee(futurePosition)

    def doPursuit(self, target):
        distance = target - self.host.position

        updatesNeeded = distance.get_length() / self.host.max_velocity

        targetFuturePosition = target + (Vec2d(0, 0) * updatesNeeded)
        return self.doSeek(targetFuturePosition)
