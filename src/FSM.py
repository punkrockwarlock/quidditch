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
        # else if the chaser is not closest of team chasers then
        else:
            # change the state so that they support the chaser that is closest
            self.pop()
            self.push(self.support)

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
            # if the opponent gets the quaffle first
            if self.parent.opposition.has(self.game.quaffle.getPossession()):
                self.pop()
                self.push(self.defend)

            closest_chaser = functions.groupClosest(self.parent.chasers,
                                                self.game.quaffle)

            # if the chaser is not the closest of team chasers then
            if closest_chaser != self:
                # change the state so that they support closest chaser
                self.pop()
                self.push(self.support)

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
        # if within shooting range of goal
        if functions.distance(self.parent, self.parent.goal[1]) <= self.parent.getShootDist():
            # change to shoot state
            self.pop()
            self.push(self.shoot)
        # if no longer in possession
        if self.game.quaffle.possession != self:
            # change to default state
            self.pop()
            self.push(self.default)

    def support_attack(self):
        """ Implements the behaviour of flying to towards the goal when not in
            possession and staying close to chaser with quaffle so that they
            can pass to me """

        # this needs to change so it seeks open space near chaser with quaffle
        self.parent.steerMngr.seek(self.parent.goal[1])
        self.parent.steerMngr.collisionAvoidance()

        if not self.parent.team.has(self.game.quaffle.possession):
            self.pop()
            self.push(self.default)

    def defend(self):
        """ Implements behaviour of defending when opposition has possession """

        # if closest to player with quaffle
            # change state to tackle
        # if opposition lose possession
            # change state to default
