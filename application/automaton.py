import base64
import os
from pyvis.network import Network

from application.specification_exception import SpecificationException


class Transition:
    def __init__(self, input_value, end_state, isInput):
        self.end_state = None
        self.input_value = input_value
        self.end_state = end_state
        self.isInput = isInput

    def copy(self):
        return Transition(self.input_value, self.end_state, self.isInput, )

    def __repr__(self):
        return f"({self.input_value if self.input_value is not None else 'None'} {'?' if self.isInput else '!'})--> {self.end_state}"

class StateGenerator:
    def __init__(self):
        self.states = []
        self.state_count = 0

    def add_state(self,name,color = None):
        state = State(f"{name} - {self.state_count})", color)
        self.states.append(state)
        self.state_count += 1
        return state
class State:
    def __init__(self, name,color = None):
        self.name = name
        self.color = color
        self.input_transitions: [Transition] = [Transition("None", self,
                                                           True)]  # the input transition will always go to itself, because if you do nothing the output will always decide what will be done
        self.output_transitions: [Transition] = []
        self.is_winning = False

    def get_score(self):
        return 1 if self.is_winning else 0

    def addTransition(self, transition: Transition):
        if transition.isInput:
            self.input_transitions.append(transition)
        else:
            self.output_transitions.append(transition)

    def is_terminal(self):
        return self.output_transitions == []

    def getTransitions(self):
        transitions = []
        for transition in self.input_transitions:
            transitions.append(transition)
        for transition in self.output_transitions:
            transitions.append(transition)
        return transitions

    def addTransitions(self, *transitions: [Transition]):
        for transition in transitions:
            self.addTransition(transition)

    def shallow_copy(self):
        return State(self.name)

    def __repr__(self):
        return self.name


class FSM:
    def __init__(self, states: [State], initial_state: State):
        self.states = states
        self.current_state = initial_state
        self.initial_state = initial_state

    def process_data(self, input_value, is_input):
        self.current_state = self.process_data_from_state(self.current_state, input_value, is_input)

    def process_data_from_state(self, state: State, input_value, is_input):
        for transition in state.input_transitions if is_input else state.output_transitions:
            if transition.input_value == input_value:
                # print(f"Transition: {state} --({input_value})--> {transition.end_state}")
                return transition.end_state
        raise SpecificationException(
            f"No valid transition for {'input' if is_input else 'output'} '{input_value}' in state '{state}'.")


    def showFsm(self):
        #multiple self loops are on top of eachother
        net = Network(notebook=False, cdn_resources="remote",
                      bgcolor="#222222",
                      font_color="white",
                      height="750px",
                      width="100%",
                      directed=True
                      )
        net.force_atlas_2based(gravity=-273, central_gravity=0.015, spring_length=500)
        for state in self.states:
            net.add_node(str(state), label=f"{state} - {state.get_score()}",color=state.color)
        for state in self.states:
            for transition in state.getTransitions():
                label = str(transition.input_value)
                label = label if len(label) < 5 else f"{label[:5]}..."

                label = label + "?" if transition.isInput else label + "!"

                net.add_edge(str(state), str(transition.end_state), label=label)

        net.set_edge_smooth("dynamic")

        net.show(os.path.join("../data", "specification_graph.html"),notebook=False)



    def __repr__(self):
        text = ""
        for state in self.states:
            text += f"{state}\n"
            for transition in state.getTransitions():
                text += f"\t{transition}\n"
        return text

    # Example usage


if __name__ == "__main__":
    # Define states
    state_a = State("A")
    state_b = State("B")
    state_c = State("C")

    # Define transitions

    state_a.addTransitions(Transition('c?', state_b),
                           Transition('c!', state_c))
    state_b.addTransitions(Transition('c?', state_a),
                           Transition('c!', state_c))
    state_c.addTransitions(Transition('c?', state_b),
                           Transition('c!', state_a))

    # Create FSM
    fsm = FSM([state_a, state_b, state_c], state_a)

    # Process input sequence
    input_sequence = ['c?', 'c!', 'c?', 'c!', 'c?', 'c!']
    for input_value in input_sequence:
        fsm.showFsm()
        fsm.process_input(input_value)
    fsm.showFsm()
