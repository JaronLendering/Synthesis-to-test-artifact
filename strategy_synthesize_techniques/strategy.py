from application.automaton import State, Transition


class StrategyTransition:
    def __init__(self,starting_state: State, end_state: State, input_value, output_value):
        self.starting_state = starting_state
        self.end_state = end_state
        self.input_value = input_value
        self.output_value = output_value

class Strategy:
    def __init__(self, goal_state: State):
        self.transitions: {} = {} # (starting_state, input)
        self.goal_state = goal_state

    def add_transitions(self, state, input):
        self.transitions.update({state: input})

    def repr_as_image(self):
        pass
    def __repr__(self, level=0):
        ret = ""
        for key in self.transitions.keys():
            ret += f"{key}: {self.transitions[key]}\n"
        return ret

    def return_input(self, state: State):
        return self.transitions.get(state)
