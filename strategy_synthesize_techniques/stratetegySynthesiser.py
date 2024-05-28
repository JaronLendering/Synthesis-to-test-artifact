from application.automaton import FSM, Transition, State
from application.dummySpecification import DummySpecification
from strategy_synthesize_techniques.strategy import Strategy
from test_execution_files.InputOutputProcessing import assumption_processing_transition
from abc import ABC, abstractmethod


class StrategySynthesiser(ABC):
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
            self.strategy_synthesize(self.specification_automaton.initial_state,strategies[-1])
            state.score = 0
        return strategies

    @abstractmethod
    def strategy_synthesize(self,initial_state,strategy,**kwargs):
        pass

