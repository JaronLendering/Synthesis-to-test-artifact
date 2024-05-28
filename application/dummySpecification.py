from application.automaton import FSM, State, Transition


class DummySpecification():
    def __init__(self):
        states = self.create_states()
        self.fsm = FSM(states,states[0])

    def create_states(self) -> [State]:
        state_zero = State('Total beginning')
        state_start = State('start')
        state_wait = State('waiting')
        state_finish = State('finished')
        state_timeout = State('timeout')
        state_stop_music = State('stop music')
        state_start_music = State('start music')
        state_loop1 = State('loop1')
        state_loop2 = State('loop2')
        state_middle_loop = State('middle loop')

        state_zero.addTransitions(
            Transition("loop", state_middle_loop, True),
            Transition("start",state_start,True),
            Transition("None",state_zero,False)
        )
        state_start.addTransitions(
            Transition("give 0 for starting music and 1 for stopping music", state_wait, False)
        )
        state_middle_loop.addTransitions(

            Transition("L2", state_loop2, True),
            Transition("L1", state_loop1, False),
            Transition("None",state_middle_loop,False)
        )
        state_loop1.addTransitions(
            Transition("L1 back", state_middle_loop,False)
        )
        state_loop2.addTransitions(
            Transition("L2 back", state_middle_loop,False)
        )
        state_wait.addTransitions(
            Transition("0", state_start_music, True),
            Transition("1", state_stop_music, True),
            Transition('None', state_timeout, False),
            Transition("f", state_finish, False),

        )
        return [state_zero,
                state_start,
                state_wait,
                state_finish,
                state_timeout,
                state_stop_music,
                state_start_music,
                state_loop1,
                state_loop2,
                state_middle_loop
               ]



if __name__ == "__main__":
    c = DummySpecification()
    c.fsm.showFsm()