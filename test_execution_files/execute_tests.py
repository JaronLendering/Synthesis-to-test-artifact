from ..strategy_synthesize_techniques.strategy import Strategy
from ..application.automaton import FSM
class ExecuteTests():
    def __init__(self,strategies: [Strategy], application: FSM):
        self.strategies = strategies
        self.application = application

