import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

class Transition:
    def __init__(self, input_value, end_state, isInput, part_of: bool = False):
        self.input_value = input_value
        self.end_state = end_state
        self.part_of = part_of
        self.isInput = isInput

    def copy(self):
        return Transition(self.input_value, self.end_state, self.isInput, self.part_of)

    def __repr__(self):
        return f"({self.input_value if self.input_value is not None else 'None' } {'?' if self.isInput else '!'})--> {self.end_state}"

class State:
    def __init__(self, name):
        self.name = name
        self.input_transitions: [Transition] = []
        self.output_transitions: [Transition] = []
        self.score = None


    def addTransition(self, transition: Transition):
        if transition.isInput:
            self.input_transitions.append(transition)
        else:
            self.output_transitions.append(transition)

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

    def process_data(self, input_value,is_input):
        for transition in self.current_state.input_transitions if is_input else self.current_state.output_transitions:
            if (transition.input_value == input_value): #TODO: make it check if a transition is in a message or is the message
                print(f"Transition: {self.current_state} --({input_value})--> {transition.end_state}")
                self.current_state = transition.end_state
                return True
        raise Exception(f"No valid transition for input '{input_value}' in state '{self.current_state}'.")

    def better_show_fsm(self):
        fsm = nx.DiGraph()
        node_size = 2000
        for state in self.states:
            for transition in state.getTransitions():
                fsm.add_edge(state, transition.end_state, label=transition.input_value,
                             is_input=transition.isInput)
        layout = graphviz_layout(fsm, prog='dot')

        nx.draw_networkx_nodes(fsm, layout, node_size=node_size,
                               node_color=["red" if i == self.states.index(self.current_state) else "gray" for i in
                                           range(len(self.states))])
        nx.draw_networkx_labels(fsm, layout)
        for edge in fsm.edges():
            nx.draw_networkx_edges(
                fsm, layout, edgelist=[edge], edge_color='gray', arrows=True,
                arrowsize=20, node_size=node_size)
            edge_data = fsm.get_edge_data(edge[0], edge[1])
            is_input = edge_data["is_input"]
            label = str(edge_data["label"])
            label = label if len(label) < 5 else f"{label[:5]}..."
            label = label + "?" if is_input == True else label + "!"
            edge_labels = {edge: label}
            nx.draw_networkx_edge_labels(fsm, layout, edge_labels=edge_labels,
                                         connectionstyle=fsm.get_edge_data(edge[0], edge[1])['connectionstyle'])
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    def showFsm(self):
        fsm = nx.DiGraph()
        node_size = 2000

        for state in self.states:
            for transition in state.getTransitions():
                if fsm.has_edge(transition.end_state,state):
                    fsm.add_edge(state,transition.end_state,label = transition.input_value,connectionstyle='arc3,rad=-0.2',is_input = transition.isInput)
                    other_label = fsm.edges[transition.end_state,state]["label"]
                    is_input = fsm.edges[transition.end_state,state]["is_input"]
                    fsm.remove_edge(transition.end_state,state)
                    fsm.add_edge(transition.end_state, state, label=other_label,
                                 connectionstyle='arc3,rad=-0.2', is_input = is_input )
                else:
                    fsm.add_edge(state,transition.end_state,label = transition.input_value,connectionstyle='arc3,rad=0', is_input = transition.isInput)

        layout = nx.circular_layout(fsm)

        nx.draw_networkx_nodes(fsm, layout,node_size=node_size,node_color = ["red" if i == self.states.index(self.current_state) else "gray" for i in range(len(self.states))])
        nx.draw_networkx_labels(fsm, layout)
        for edge in fsm.edges():
            nx.draw_networkx_edges(
                fsm, layout, edgelist=[edge], edge_color='gray', arrows=True,
                arrowsize=20, node_size=node_size,connectionstyle=fsm.get_edge_data(edge[0], edge[1])['connectionstyle']
            )
            edge_data = fsm.get_edge_data(edge[0], edge[1])
            is_input = edge_data["is_input"]
            label = str(edge_data["label"])
            label = label if len(label) < 5  else f"{label[:5]}..."
            label = label + "?" if is_input == True else label + "!"
            edge_labels = {edge: label}
            nx.draw_networkx_edge_labels(fsm,layout,edge_labels= edge_labels,connectionstyle=fsm.get_edge_data(edge[0], edge[1])['connectionstyle'])
        plt.axis('off')
        plt.tight_layout()
        plt.show()

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
    input_sequence = ['c?','c!','c?','c!','c?','c!']
    for input_value in input_sequence:
        fsm.showFsm()
        fsm.process_input(input_value)
    fsm.showFsm()
