from application.automaton import State, Transition
from application.dummySpecification import DummySpecification
from strategy_synthesize_techniques.strategy import Strategy
from strategy_synthesize_techniques.stratetegySynthesiser import StrategySynthesiser
from test_execution_files.InputOutputProcessing import *


class BiStrategySynthesiser(StrategySynthesiser):
    def strategy_synthesize(self, current_state: State, strategy: Strategy, seen_states=None):
        if seen_states is None:
            seen_states = []

        test_actions = current_state.input_transitions
        tested_actions = current_state.output_transitions
        overall_action_score = (0, None)  # score, test_action
        if current_state.score == 1:
            return 1
        if current_state in seen_states:
            return 0
        seen_states.append(current_state)

        for test_action in test_actions + [Transition(None, current_state, True)]:
            action_score = 0

            for tested_action in tested_actions:
                transition = assumption_processing_transition(test_action, tested_action)
                new_state = self.specification_automaton.process_data_from_state(current_state, transition.input_value,
                                                                                 transition.isInput)
                action_score += self.strategy_synthesize(new_state, strategy, seen_states)
            if overall_action_score[0] < action_score:
                overall_action_score = (action_score, test_action.input_value)
        strategy.add_transitions(current_state, overall_action_score[1])

        return overall_action_score[0]


if __name__ == "__main__":
    synthesiser = StrategySynthesiser(DummySpecification().fsm)
    strategies = synthesiser.synthesize_all_backward_induction()

    for strategy in strategies:
        print(f"\t{strategy.goal_state}")
        print(strategy)