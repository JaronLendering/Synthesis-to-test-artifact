from application.automaton import FSM, Transition
from application.dummySpecification import DummySpecification


def spec_to_game(specification: FSM) -> FSM:
    states = specification.states
    copy_states = [state.shallow_copy() for state in states]
    for state,new_state in zip(states,copy_states):
        transitions = []
        for input_tran in state.input_transitions:
            for output_tran in state.output_transitions:
                if output_tran.input_value is None:
                    transitions.append(input_tran.copy())
                    transitions.append(Transition("None",input_tran.end_state,False))
                else:
                    transitions.append(output_tran.copy())
                    transitions.append(Transition(input_tran.input_value,output_tran.end_state,True, input_tran.part_of))
        new_state.addTransitions(*transitions)
    return FSM(copy_states,copy_states[0])

if __name__ == "__main__":
    game = (DummySpecification().fsm)
    print(game)