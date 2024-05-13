class Transition:
    def __init__(self, input_value, end_state):
        self.input_value = input_value
        self.end_state = end_state


class State:
    def __init__(self, name):
        self.name = name
        self.transitions = []

    def addTransition(self, transition: Transition):
        self.transitions.append(transition)

    def addTransitions(self, transitions: [Transition]):
        self.transitions.extend(transitions)

    def __repr__(self):
        return self.name


class FSM:
    def __init__(self, states: [State], initial_state: State):
        self.states = states
        self.current_state = initial_state

    def process_input(self, input_value):
        for transition in self.current_state.transitions:
            if (transition.input_value == input_value):
                print(f"Transition: {self.current_state} --({input_value})--> {transition.end_state}")
                self.current_state = transition.end_state
                return True
        print(f"No valid transition for input '{input_value}' in state '{self.current_state}'.")
        return False


# Example usage
if __name__ == "__main__":
    # Define states
    state_a = State("A")
    state_b = State("B")
    state_c = State("C")

    # Define transitions

    state_a.addTransitions([Transition('c?', state_b),
                            Transition('c!', state_c)])
    state_b.addTransitions([Transition('c?', state_a),
                            Transition('c!', state_c)])
    state_c.addTransitions([Transition('c?', state_b),
                            Transition('c!', state_a)])

    # Create FSM
    fsm = FSM([state_a, state_b, state_c], state_a)

    # Process input sequence
    input_sequence = ['c?','c!','c?','c!','c?','c!','a']
    for input_value in input_sequence:
        fsm.process_input(input_value)
