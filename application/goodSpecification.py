from pyvis.network import Network

from application.automaton import FSM, State, Transition, StateGenerator


class GoodSpecification():
    def __init__(self):
        states = self.create_states()
        self.fsm = FSM(states,states[0])

    def create_choice_state(self,state,dept,max_dept,choice_amount, current_states,state_generator,choice_number=""):

        if dept < max_dept:
            state.addTransition(Transition("None", state,False))
            for i in range(choice_amount):
                next_state = state_generator.add_state(f"choices node - dept {dept}")
                state.addTransition(Transition(f"next{choice_number}{i}",next_state, True )) #i < choice_amount//2
                state.addTransition(Transition(f"None",state,False))
                current_states.append(next_state)
                self.create_choice_state(next_state,dept+1,max_dept,choice_amount,current_states,state_generator,f"{choice_number}{i}")


    def create_states(self) -> [State]:
        state_generator = StateGenerator()
        state_zero = state_generator.add_state('Total beginning', "red")
        state_lines = state_generator.add_state('Line start',"blue")
        state_line_finish = state_generator.add_state('long line finish', "blue")
        long_states_lines_same_outcome = []
        for line in range(3):
            last_state = state_lines
            for state in range(20):
                node = state_generator.add_state(f"line {line} - state {state}")
                last_state.addTransition(Transition(f"go{line}", node,True))
                last_state.addTransition(Transition(f"None",last_state,False))
                last_state = node
                long_states_lines_same_outcome.append(node)
            last_state.addTransition(Transition("end",state_line_finish,True))
            last_state.addTransition(Transition(f"None", last_state, False))

        state_choices_start = state_generator.add_state('choices start',"pink")
        choices_states = []
        self.create_choice_state(state_choices_start,0,4,5,choices_states,state_generator)



        state_loop1 = state_generator.add_state('loop1')
        state_loop2 = state_generator.add_state('loop2')
        state_middle_loop = state_generator.add_state('middle loop', "purple")

        state_middle_loop.addTransitions(

            Transition("L2", state_loop2, True),
            Transition("L1", state_loop1, False),
            Transition("None", state_middle_loop, False)
        )
        state_loop1.addTransitions(
            Transition("L1 back", state_middle_loop,False)
        )
        state_loop2.addTransitions(
            Transition("L2 back", state_middle_loop,False)
        )

        state_zero.addTransitions(
            Transition("lines",state_lines,True),
            Transition("choices", state_choices_start,True),
            Transition("loop", state_middle_loop,True),
            Transition("None", state_zero, False)

        )


        return state_generator.states



if __name__ == "__main__":
    c = GoodSpecification()
    c.fsm.states[2].is_winning = True
    print(c.fsm.initial_state.getTransitions())
    c.fsm.showFsm()
