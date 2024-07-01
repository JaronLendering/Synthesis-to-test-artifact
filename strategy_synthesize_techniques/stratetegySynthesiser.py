
from application.automaton import FSM, Transition, State
from application.dummySpecification import DummySpecification
from application.goodSpecification import GoodSpecification
from strategy_synthesize_techniques.mctsTree import MctsTree, ActionChooserEnum
from strategy_synthesize_techniques.biStrategy import BiStrategy
from strategy_synthesize_techniques.strategy import Strategy
from strategy_synthesize_techniques.strategySynthesizerEnum import StrategySynthesizerChooser
from test_execution_files.InputOutputProcessing import assumption_processing_transition


class StrategySynthesiser():
    def __init__(self,specification: FSM, name: StrategySynthesizerChooser):
        self.specification_automaton = specification
        self.strategy_synthesizer = self.get_synthesizer(name)
        self.synthesizer_kind = name
        self.iteration_count = 30
        self.max_select_recursion = 50
        self.max_rollout_recursion = 12
        self.action_chooser = ActionChooserEnum.RANDOM

    def get_synthesizer(self, name):
        self.synthesizer_kind = name
        match name:
            case StrategySynthesizerChooser.BI:
                return self.bi_strategy_synthesize_all
            case StrategySynthesizerChooser.SM_MCST:
                return self.SM_MCTS_strategy_synthesize_all
            case _:
                raise Exception(f"{name} is not a strategy synthesize technique")


    def set_MCTS_configuration_values(self,iteration_count = None,max_select_recursion = None,max_rollout_recursion = None):
        if iteration_count is not None:
            self.iteration_count = iteration_count
        if max_select_recursion is not None:
            self.max_select_recursion = max_select_recursion
        if max_rollout_recursion is not None:
            self.max_rollout_recursion = max_rollout_recursion


    def bi_strategy_synthesize_all(self) -> [Strategy]:
        states = self.specification_automaton.states
        strategies = []
        for state in states:
            state.is_winning = True
            strategy = BiStrategy(state)
            self.bi_strategy_synthesize(self.specification_automaton.initial_state,strategy)
            strategies.append(strategy)
            state.is_winning = False
        return strategies



    def SM_MCTS_strategy_synthesize_all(self) -> [Strategy]:
        states = self.specification_automaton.states
        strategies = []
        for state in states:
            state.is_winning = True
            strategy = MctsTree(state,self.specification_automaton.initial_state,None,self.specification_automaton,self.action_chooser)
            for i in range(self.iteration_count):
                self.SM_MCTS_strategy_synthesize(strategy,self.max_select_recursion)
            strategies.append(strategy)
            state.is_winning = False
        return strategies


    def SM_MCTS_strategy_synthesize(self, strategy: MctsTree, select_recursion_left ):

        if strategy.state.is_winning or strategy.state.is_terminal():
            return strategy.state.get_score()
        unchecked_transition = strategy.get_unchecked_transition()
        if unchecked_transition is not None:
            test_action, tested_action = unchecked_transition
            transition = assumption_processing_transition(test_action, tested_action)
            new_state = self.specification_automaton.process_data_from_state(strategy.state, transition.input_value, transition.isInput)
            new_strategy = strategy.summon_child(new_state)

            score = new_strategy.rollout(self.specification_automaton,self.max_rollout_recursion)

            strategy.duct_update(test_action, tested_action,score)
            return score
        test_action, tested_action = strategy.duct_select()
        transition = assumption_processing_transition(test_action, tested_action)
        new_state = self.specification_automaton.process_data_from_state(strategy.state, transition.input_value,
                                                                         transition.isInput)

        new_strategy = strategy.summon_child(new_state)

        score = self.SM_MCTS_strategy_synthesize(new_strategy,select_recursion_left-1) if select_recursion_left > 0 else strategy.state.get_score()
        strategy.duct_update(test_action, tested_action, score)

        return score

    def bi_strategy_synthesize(self, current_state: State, strategy: BiStrategy, seen_states=None):
        if strategy is None:
            strategy = BiStrategy(current_state)
        if seen_states is None:
            seen_states = []

        test_actions = current_state.input_transitions
        tested_actions = current_state.output_transitions
        overall_action_score = (0, None)  # score, test_action
        if current_state.is_winning:
            return current_state.get_score()

        if current_state in seen_states:
            input_and_score = strategy.transitions.get(current_state) # this makes sure that the score the state got, is properly propagated through the state beforehand
            return input_and_score[1] if input_and_score is not None else current_state.get_score()
        seen_states.append(current_state)

        for test_action in test_actions:
            action_score = current_state.get_score()

            for tested_action in tested_actions:
                transition = assumption_processing_transition(test_action, tested_action)
                new_state = self.specification_automaton.process_data_from_state(current_state, transition.input_value,
                                                                                 transition.isInput)
                action_score += self.bi_strategy_synthesize(new_state, strategy, seen_states)
            action_score = action_score/len(tested_actions) if len(tested_actions) > 0 else action_score
            if overall_action_score[0] < action_score:
                overall_action_score = (action_score, test_action.input_value)
        strategy.add_transitions(current_state, overall_action_score[1],overall_action_score[0])

        return overall_action_score[0]





if __name__ == "__main__":

    for i in range(1):
        strategies = StrategySynthesiser(GoodSpecification().fsm,"BI").strategy_synthesizer()
    #strategies[1].show()
    print(f"\t{strategies[1].goal_state}\n")
    print(strategies[1])
