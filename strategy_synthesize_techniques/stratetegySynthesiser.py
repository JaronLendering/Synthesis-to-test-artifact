from application.automaton import FSM, Transition, State
from application.dummySpecification import DummySpecification
from strategy_synthesize_techniques.strategy import Strategy
from test_execution_files.InputOutputProcessing import assumption_processing_transition


class StrategySynthesiser(object):
    def __init__(self,specification: FSM):
        self.specification_automaton = specification


    """
    It synthesizes as many strategies as there are nodes. 
    In every strategy, a unique node will be the goal state. 
    """
    def synthesize_all_backward_induction(self) -> [Strategy]:
        states = self.specification_automaton.states
        strategies = []
        for state in states:
            state.score = 1
            strategies.append(Strategy(state))
            self.backward_induction(self.specification_automaton.initial_state,strategies[-1])
            state.score = 0
        return strategies


    def backward_induction(self, current_state: State, strategy: Strategy):
            test_actions = current_state.input_transitions
            tested_actions = current_state.output_transitions
            overall_action_score = (0,None) # score, test_action

            if current_state.score == 1:
                return 1

            for test_action in test_actions + [Transition(None, current_state, True)]:
                action_score = 0
                for tested_action in tested_actions:
                    transition = assumption_processing_transition(test_action, tested_action)
                    new_state = self.specification_automaton.process_data_from_state(current_state, transition.input_value,
                                                                                     transition.isInput)
                    action_score += self.backward_induction(new_state,strategy)
                if overall_action_score[0] < action_score:
                    overall_action_score = (action_score,test_action)
            strategy.add_transitions(current_state, overall_action_score[1])

            return overall_action_score[0]





if __name__ == "__main__":
    synthesiser = StrategySynthesiser(DummySpecification().fsm)
    strategies = synthesiser.synthesize_all_backward_induction()

    for strategy in strategies:
        print(strategy.goal_state)
        print(f"\t{strategy}")