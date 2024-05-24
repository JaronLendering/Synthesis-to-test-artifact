from application.automaton import FSM, State, Transition


class DummySpecification():
    def __init__(self):
        states = self.create_states()
        self.fsm = FSM(states,states[0])

    def create_states(self) -> [State]:
        state_start = State('start')
        state_wait = State('waiting')
        state_finish = State('finished')
        state_timeout = State('timeout')
        state_stop_music = State('stop music')
        state_start_music = State('start music')

        state_start.addTransitions(
            Transition("give 0 for starting music and 1 for stopping music", state_wait, False)
        )
        state_wait.addTransitions(
            Transition("0", state_start_music, True),
            Transition("1", state_stop_music, True),
            Transition(None, state_timeout, False),
            Transition("f", state_finish, False)
        )
        return [state_start, state_wait, state_stop_music, state_start_music,state_finish,state_timeout]


c = DummySpecification()
c.fsm.showFsm()