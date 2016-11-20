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
        # - if quaffle free:
        if self.parent.game.quaffle.possession is None:
            # state:- get_quaffle()
            self.push(self.get_quaffle)
        # - elif me has quaffle:
        elif self.parent.possession is not None:
            # state:- attack_goal()
            self.push(self.attack_goal)
        # - elif team has quaffle:
        elif self.parent.team.has(self.parent.game.quaffle.possession):
            # state:- support_attack()
            self.push(self.support_attack)
        # - else opposition has quaffle:
        else:
            # state:- defend()
            self.push(self.defend)

    def get_quaffle(self):
        
