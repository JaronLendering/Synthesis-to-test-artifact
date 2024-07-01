from pyvis.network import Network

from application import stateTypes
from application.automaton import FSM, State, Transition, StateGenerator
from application.specTypes import SpecTypes
from application.stateTypes import StateTypes


class GoodSpecification():

    def __init__(self,lines = False, choices = False, loop = False):
        initial_state,state_generator = self.create_states(lines,choices,loop)
        self.fsm = self.get_spec_fsm(initial_state,state_generator)
        self.type = SpecTypes.GOOD
    def get_spec_fsm(self, initial_state: State, state_generator: [StateGenerator]):
        return FSM(state_generator.states,initial_state)
    def create_choices(self, state, dept, max_dept, choice_amount, current_states, state_generator, choice_number=""):
        colors = ["purple","brown","blue","green"]
        if dept < max_dept:
            state.addTransition(Transition("None", state,False))
            for i in range(choice_amount):
                next_state = state_generator.add_state(f"choices node - dept {dept}",colors[dept],type=StateTypes.CHOICES)
                state.addTransition(Transition(f"next{choice_number}{i}",next_state, True )) #i < choice_amount//2
                current_states.append(next_state)
                self.create_choices(next_state, dept + 1, max_dept, choice_amount, current_states, state_generator, f"{choice_number}{i}")

    def create_line_states(self,state_generator):
        state_lines = state_generator.add_state('Line start', "green",StateTypes.LINES)
        state_lines.addTransition(Transition(f"None", state_lines, False))
        state_line_finish = state_generator.add_state('long line finish', "yellow",StateTypes.LINES)
        long_states_lines_same_outcome = []
        for line in range(3):
            last_state = state_lines
            for state in range(20):
                node = state_generator.add_state(f"line {line} - state {state}","green",StateTypes.LINES)
                last_state.addTransition(Transition(f"go{line}", node, True))
                if last_state != state_lines:
                    last_state.addTransition(Transition(f"None", last_state, False))
                last_state = node
                long_states_lines_same_outcome.append(node)
            last_state.addTransition(Transition("end", state_line_finish, True))
            last_state.addTransition(Transition(f"None", last_state, False))

        return state_lines, state_generator

    def create_choice_states(self,state_generator):
        state_choices_start = state_generator.add_state('choices start', "pink", StateTypes.CHOICES)
        choices_states = []
        self.create_choices(state_choices_start, 0, 4, 5, choices_states, state_generator)
        return state_choices_start,state_generator

    def create_loop_states(self,state_generator):
            state_middle_loop = state_generator.add_state('middle loop', "purple",StateTypes.LOOP)
            state_side_loop = state_generator.add_state('side loop', "purple", StateTypes.LOOP)
            state_loop1 = state_generator.add_state('loop1',"purple",StateTypes.LOOP)
            state_loop2 = state_generator.add_state('loop2',"purple",StateTypes.LOOP)

            state_middle_loop.addTransitions(

                Transition("L2", state_loop2, True),
                Transition("L1", state_loop1, False),
                Transition("None", state_middle_loop, False)
            )

            state_side_loop.addTransitions(
                Transition("L2", state_loop2, True),
                Transition("L1", state_loop1, True),
                Transition("None", state_side_loop, True)
            )
            state_loop1.addTransitions(
                Transition("L1 back", state_middle_loop, False)
            )
            state_loop2.addTransitions(
                Transition("L2 back", state_middle_loop, False)
            )
            return [state_middle_loop, state_side_loop], state_generator

    def create_states(self, lines = False, choices = False, loop = False) -> [State]:
        if not lines and not choices and not loop:
            lines = True
            choices = True
            loop = True
        state_generator = StateGenerator()
        state_zero = state_generator.add_state('Total beginning', "red",StateTypes.START)
        state_zero.addTransition(Transition("None", state_zero, False))
        if lines == True:
            state_lines = self.create_line_states(state_generator)[0]
            state_zero.addTransition(Transition("lines",state_lines,True))
        if loop == True:
            state_gen_loop_return = self.create_loop_states(state_generator)[0]

            state_middle_loop = state_gen_loop_return[0]
            state_side_loop = state_gen_loop_return[1]
            state_zero.addTransition(Transition("loop", state_middle_loop,True))
            state_zero.addTransition(Transition("side loop", state_side_loop,True))

        if choices == True:
            state_choices_start = self.create_choice_states(state_generator)[0]
            state_zero.addTransition(Transition("choices", state_choices_start,True))





        return state_zero, state_generator




if __name__ == "__main__":
    c = GoodSpecification()
    initial_state,state_generator = c.create_states(choices=True)
    fsm = c.get_spec_fsm(initial_state, state_generator)
    #print(fsm.initial_state.getTransitions())
    fsm.showFsm()
