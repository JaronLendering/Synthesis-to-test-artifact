import threading

from application.catchStateChanges import catchStateChanges
from application.dummyApplication import DummyApplication
from application.dummySpecification import DummySpecification
from strategy_synthesize_techniques.strategy import Strategy
from application.automaton import FSM


class ExecuteTests():
    def __init__(self, strategies: [Strategy], application: DummyApplication, specification: FSM):
        self.strategies = strategies
        self.application = application
        self.specification = specification

    def runTest(self):
        self.validateStrategies()
        state_changed = threading.Condition()
        logger = catchStateChanges(state_changed)
        logger.catchAllOutput()
        for strategy in self.strategies:
            self.traverse_strategy(strategy, logger, state_changed)

    def traverse_strategy(self, strategy, logger, state_changed):
        if logger.print_queue == []:
            state_changed.wait()
        output = logger.logger.printDequeue()
        new_state,input = strategy.process(output)
        #strategy processes it as :
        # If output is None -> give an input that you want to do
        # else input = None
        # I make this output eager
        self.specification.process_data(output,False)
        self.specification.process_data(input, True)
        self.application.process_data(input)
        self.traverse_strategy(new_state, logger, state_changed)

    def validateStrategies(self):
        for strategy in self.strategies:
            self.transitionChecker(strategy)

    def transitionChecker(self, root: Strategy):
        supposedTransitionKind = 0
        for (child, action, isInput) in root.children:
            currentTransitionKind = 1 if isInput else -1
            if supposedTransitionKind == 0:
                supposedTransitionKind = currentTransitionKind
            elif supposedTransitionKind == 1:
                raise Exception(
                    "Multiple input transitions are possible from the same state")  # because I write code as if it always has 1 optimal way
            self.transitionChecker(child)
