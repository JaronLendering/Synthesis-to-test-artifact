from application.automaton import FSM
from application.dummySpecification import DummySpecification
from strategy import Strategy
class StrategySynthesiser(object):
    def __init__(self,specification: FSM):
        self.specification_automaton = specification
        pass

    def synthesize(self) -> Strategy:
        end
        for state in self.specification_automaton.states:
