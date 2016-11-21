import functions


class FSM:
    """To be inherited"""
    def __init__(self, parent):
        self.parent = parent
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

    def default(self):
        # if nobody has the quaffle
        if self.parent.game.quaffle.possession is None:
            # change state to get the quaffle
            self.push(self.get_quaffle)
        # else if I have the quaffle
        elif self.parent.possession is not None:
            # change state to attack the goal
            self.push(self.attack_goal)
        # else if my team has the quaffle
        elif self.parent.team.has(self.parent.game.quaffle.possession):
            # change state to support attack
            self.push(self.support_attack)
        # else the opposition has the quaffle
        else:
            # change state to defend
            self.pop()
            self.push(self.defend)

    def get_quaffle(self):
        """ Implements the behaviour of chasing a quaffle that is not in
            possession, only the closest chaser will go after the quaffle.
            All others revert to default state """

        # get the closest chaser from my team
        closest_chaser = functions.groupClosest(self.parent.chasers,
                                                self.parent.game.quaffle)

        # if I am the closest chaser
        if closest_chaser == self:
            # move towards the quaffle
            self.parent.steerMngr.seek(self.parent.game.quaffle)
        else:
            # revert to default state, !!might need to change this!!
            self.pop()
            self.push(self.default)

    def attack_goal(self):
        """ Implements the behaviour of flying towards the goal when in
            possession, and shooting when within range, or passing when
            opposition is too close. If shoot, pass or lose possession revert
            to default state """

        # seek towards goal
        self.parent.steerMngr.seek(self.parent.goal[1])

        # avoid opposition
        self.parent.steerMngr.collisionAvoidance()

        # if opposition chaser is too close
        if functions.groupClosest(self.parent.game.get_team(self.parent.opposition), self):
            # change to pass state
            self.pop()
            self.push(self.pass_quaffle)
        # if within shooting range of goal
        if functions.distance(self.parent, self.parent.goal[1]) <= self.parent.getShootDist():
            # change to shoot state
            self.pop()
            self.push(self.shoot)
        # if no longer in possession
        if self.parent.game.quaffle.possession != self:
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

        if not self.parent.team.has(self.parent.game.quaffle.possession):
            self.pop()
            self.push(self.default)

    def defend(self):
        """ Implements behaviour of defending when opposition has possession """

        # if closest to player with quaffle
            # change state to tackle
        # if opposition lose possession
            # change state to default
