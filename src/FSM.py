import functions
import constants as const


class FSM:
    """To be inherited"""
    def __init__(self, parent):
        self.parent = parent
        self.game = parent.game
        self.stateStack = []

    def pop(self):
        return self.stateStack.pop()

    def push(self, state):
        self.stateStack.append(state)

    def update(self):
        current = self.stateStack[len(self.stateStack) - 1]
        current()


class fsm_Chaser(FSM):
    def __init__(self, parent):
        FSM.__init__(self, parent)

    def free_quaffle(self):
        """ this state is triggered when the quaffle is not in possession """

        closest_chaser = functions.groupClosest(self.parent.chasers,
                                                self.game.quaffle)

        # if the chaser is the closest of team chasers then
        if closest_chaser == self:
            # change the state so that they seek the quaffle
            self.pop()
            self.push(self.get_quaffle)
            return
        # else if the chaser is not closest of team chasers then
        else:
            # change the state so that they support the chaser that is closest
            self.pop()
            self.push(self.support)
            return

    def get_quaffle(self):
        """ Implements the behaviour of chasing a quaffle that is not in
            possession, only the closest chaser will go after the quaffle.
            All others will go to support state """

            # steer towards the quaffle
            self.parent.steerMngr.seek(self.game.quaffle)
            self.avoidCollisions()

            # if I am close enough to the quaffle to grab it
            if distance(self.game.quaffle, self) <= const.GRAB_DISTANCE:
                # and the quaffle is not is possession
                if not self.game.quaffle.inPossession():
                    # grab the quaffle and change state to attack
                    self.game.quaffle.setPossession(self.parent)
                    self.pop()
                    self.push(self.attack_goal)
                    return
            # if the opponent gets the quaffle first
            if self.parent.opposition.has(self.game.quaffle.getPossession()):
                self.pop()
                self.push(self.defend)
                return

            # if the chaser is not the closest of team chasers then
            if functions.groupClosest(self.parent.chasers, self.game.quaffle) != self:
                # change the state so that they support closest chaser
                self.pop()
                self.push(self.support)
                return

    def attack_goal(self):
        """ Implements the behaviour of flying towards the goal when in
            possession, and shooting when within range, or passing when
            opposition is too close. If shoot, pass or lose possession revert
            to default state """

        # seek towards goal
        self.parent.steerMngr.seek(self.parent.goal[1])
        self.parent.steerMngr.collisionAvoidance()

        # if opposition chaser is too close
        if functions.distance(functions.groupClosest(self.game.get_team(self.parent.opposition), self)) < const.PRESSURE_DISTANCE:
            # change to pass state
            self.pop()
            self.push(self.pass_quaffle)
            return
        # if within shooting range of goal
        if functions.distance(self.parent, self.parent.goal[1]) <= self.parent.getShootDist():
            # change to shoot state
            self.pop()
            self.push(self.shoot)
            return
        # if i have been tackled
        if self.parent.tackled:
            self.pop()
            self.push(self.defend)
            return

        # if no longer in possession
        if self.game.quaffle.possession != self:
            # change to default state
            self.pop()
            self.push(self.free_quaffle)
            return

    def support_attack(self):
        """ Implements the behaviour of flying to towards the goal when not in
            possession and staying close to chaser with quaffle so that they
            can pass to me """

        # this needs to change so it seeks open space near chaser with quaffle
        # need to implement a follow steering behaviour, and prevent bunching up

        # if opposition gets the quaffle
        if self.game.get_team(self.parent.opposition).has(self.game.quaffle.getPossession()):
            self.pop()
            self.push(self.defend)
            return

        # if i lose the quaffle
        if not self.parent.team.has(self.game.quaffle.getPossession()):
            self.pop()
            self.push(self.free_quaffle)
            return

    def defend(self):
        """ Implements behaviour of defending when opposition has possession """

        # follow the closest opposition chaser
        opp_chasers = self.game.get_team(self.parent.opposition).get_group("chaser")
        closest = functions.groupClosest(opp_chasers, self)
        self.parent.steerMngr.follow(closest)                # need to implement a follow steering behaviour

        # if opposition lose possession
        if not self.game.get_team(self.parent.opposition).has(self.game.quaffle.getPossession()):
            # change state to support
            self.pop()
            self.push(self.support_attack)
            return
        # if closest to player with quaffle
        my_chasers = self.game.get_team(self).get_group("chaser")
        closest = functions.groupClosest(my_chasers, self.game.quaffle)
        if closest == self:
            # change state to tackle
            self.pop()
            self.push(self.tackle)

    def tackle(self):
        """ Implements the behaviour of getting close to chaser in possession and taking quaffle """

        # get the opposition chaser in possession
        opp_chaser = self.game.quaffle.getPossession()

        # fly towards the chaser
        self.parent.steerMngr.seek(opp_chaser.position)

        # if i am within tackle distance
        if distance(opp_chaser, self) <= const.TACKLE_DIST:
            # perform a skill check to tackle chaser
            success = self.parent.tackle(opp_chaser)
            # if successful
            if success:
                # change state to attack goal
                self.pop()
                self.push(self.attack_goal)
                return
        # if quaffle is free
        if self.game.quaffle.getPossession is None:
            # change state to quaffle_free
            self.pop()
            self.push(self.quaffle_free)
            return
        # if i am no longer the closest chaser
        my_chasers = self.game.get_team(self).get_group("chaser")
        closest = functions.groupClosest(my_chasers, self.game.quaffle)
        if closest != self:
            # change state to defend
            self.pop()
            self.push(self.defend)
            return
