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
        self.push(self.free_quaffle)

    def free_quaffle(self):
        """ this state is triggered when the quaffle is not in possession """

        my_chasers = self.game.get_team(self.parent).get_group("chaser")
        closest_chaser = functions.groupClosest(my_chasers,
                                                self.game.quaffle)

        # if the chaser is the closest of team chasers then
        if closest_chaser == self.parent:
            # change the state so that they seek the quaffle
            self.pop()
            self.push(self.get_quaffle)
            return
        # else if the chaser is not closest of team chasers then
        else:
            # change the state so that they support the chaser that is closest
            self.pop()
            self.push(self.support_attack)
            return

    def get_quaffle(self):
        """ Implements the behaviour of chasing a quaffle that is not in
            possession, only the closest chaser will go after the quaffle.
            All others will go to support state """

        # steer towards the quaffle
        self.parent.steerMngr.seek(self.game.quaffle.position)
        self.parent.steerMngr.collisionAvoidance()

        # if I am close enough to the quaffle to grab it
        if functions.distance(self.game.quaffle, self.parent) <= const.GRAB_DISTANCE:
            # and the quaffle is not is possession
            if self.game.quaffle.getPossession() is None:
                # grab the quaffle and change state to attack
                self.game.quaffle.setPossession(self.parent)
                self.pop()
                self.push(self.attack_goal)
                return
        # if the opponent gets the quaffle first
        if self.game.get_team(self.parent.opposition).has(self.game.quaffle.getPossession()):
            self.pop()
            self.push(self.defend)
            return

        # if the chaser is not the closest of team chasers then
        my_chasers = self.game.get_team(self.parent).get_group("chaser")
        if functions.groupClosest(my_chasers, self.game.quaffle) != self.parent:
            # change the state so that they support closest chaser
            self.pop()
            self.push(self.support_attack)
            return

    def attack_goal(self):
        """ Implements the behaviour of flying towards the goal when in
            possession, and shooting when within range, or passing when
            opposition is too close. If shoot, pass or lose possession revert
            to default state """

        # seek towards goal
        self.parent.steerMngr.seek(self.parent.goal[0].position)
        self.parent.steerMngr.collisionAvoidance()

        # if opposition chaser is too close
        closest = functions.groupClosest(self.game.get_team(self.parent.opposition), self.parent)
        if functions.distance(closest, self.parent) < const.PRESSURE_DISTANCE:
            print "closest baddie: ", closest.team
            # change to pass state
            self.pop()
            self.push(self.pass_quaffle)
            return
        # if within shooting range of goal
        if functions.distance(self.parent, self.parent.goal[0]) <= self.parent.getShootDist():
            # change to shoot state
            self.pop()
            self.push(self.shoot)
            return

        # if no longer in possession
        if self.game.quaffle.getPossession() != self.parent:
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

        # if we lose the quaffle
        if not self.game.get_team(self.parent.team).has(self.game.quaffle.getPossession()):
            self.pop()
            self.push(self.free_quaffle)
            return

    def defend(self):
        """ Implements behaviour of defending when opposition has possession """

        # follow the closest opposition chaser
        opp_chasers = self.game.get_team(self.parent.opposition).get_group("chaser")
        closest = functions.groupClosest(opp_chasers, self.parent)
        self.parent.steerMngr.seek(closest.position)                # need to implement a follow steering behaviour

        # if opposition lose possession
        if not self.game.get_team(self.parent.opposition).has(self.game.quaffle.getPossession()):
            # change state to support
            self.pop()
            self.push(self.support_attack)
            return
        # if closest to player with quaffle
        my_chasers = self.game.get_team(self.parent).get_group("chaser")
        closest = functions.groupClosest(my_chasers, self.game.quaffle)
        if closest == self.parent:
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
            self.push(self.free_quaffle)
            return
        # if i am no longer the closest chaser
        my_chasers = self.game.get_team(self).get_group("chaser")
        closest = functions.groupClosest(my_chasers, self.game.quaffle)
        if closest != self.parent:
            # change state to defend
            self.pop()
            self.push(self.defend)
            return

    def pass_quaffle(self):
        """ Implements the behaviour of passing the quaffle to a team chaser """

        # get the closest team chaser
        my_chasers = self.game.get_team(self.parent).get_group("chaser")
        my_chasers.remove(self.parent)
        closest = functions.groupClosest(my_chasers, self.game.quaffle)

        # seek towards closest
        self.parent.steerMngr.seek(closest.position)

        # if i lose possession
        if self.game.quaffle.getPossession() != self.parent:
            # if the quaffle is free
            if self.game.quaffle.getPossession() is None:
                # change state to quaffle_free
                self.pop()
                self.push(self.free_quaffle)
                return
            # elif opposition has quaffle
            else:
                # change state to defend
                self.pop()
                self.push(self.defend)
                return

        # if the closest is within passing distance
        if functions.distance(closest, self.parent) <= const.MAX_PASS_DIST:
            # throw the quaffle in the direction of closest
            self.parent.pass_to(closest)
            # change state to support
            self.pop()
            self.push(self.support_attack)
            return
        # else we shouldn't pass to them so
        else:
            # change state to attack_goal
            self.pop()
            self.push(self.attack_goal)
            return

    def shoot(self):
        """ Implements the behaviour of throwing the quaffle towards a goal """

        # get the closest opposition goal
        # seek towards the goal

        # if i lose possession
        if self.game.quaffle.getPossession() != self.parent:
            # if the quaffle is free
            if self.game.quaffle.getPossession() is None:
                # change state to quaffle_free
                self.pop()
                self.push(self.free_quaffle)
                return
            # elif opposition has quaffle
            else:
                # change state to defend
                self.pop()
                self.push(self.defend)
                return

        # if the goal is within shooting distance
        if functions.distance(self.parent.goal[0], self.parent) < const.MAX_SHOOT_DIST:
            # throw the quaffle in the direction of the goal
            self.parent.shoot()
            # change the state to quaffle_free
            self.pop()
            self.push(self.free_quaffle)
            return
