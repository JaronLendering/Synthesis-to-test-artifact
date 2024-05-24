import multiprocessing
import sys
import threading

from application.catchStateChanges import catchStateChanges
from application.dummyApplication import DummyApplication
from application.dummySpecification import DummySpecification
from strategy_synthesize_techniques.strategy import Strategy
from application.automaton import FSM
from strategy_synthesize_techniques.stratetegySynthesiser import StrategySynthesiser
from test_execution_files.InputOutputProcessing import *


class ExecuteTests():
    def __init__(self, strategies: [Strategy], application: DummyApplication, specification: FSM):
        self.strategies = strategies
        self.application = application
        self.specification = specification
        self.logger = catchStateChanges()
        self.input_output_processing = InputOutputProcessing()


    def runTest(self):
        self.logger.catch_all_output()
        self.input_output_processing.start_input_output_monitoring()
        self.application.set_read_input(self.input_output_processing.input_dequeue)
        for strategy in self.strategies:
            application_thread = threading.Thread(target=self.application.run,daemon=True)
            application_thread.start()
            self.traverse_strategy(strategy)
            self.reset_variables(application_thread)
        self.input_output_processing.stop_input_output_monitoring()

    def reset_variables(self,application_thread):
        self.specification.current_state = self.specification.initial_state
        self.logger.reset()
        application_thread.terminate()
    def traverse_strategy(self, strategy):
        output = self.logger.print_dequeue()
        input = strategy.return_input(self.specification.current_state)
        transition = assumption_processing_input_output(input,output)
        self.specification.process_data(transition.input_value,transition.isInput)
        self.input_output_processing.cmd_input_emulator(input)
        if not self.specification.current_state.is_terminal():
            self.traverse_strategy(strategy)
        else:
            if self.specification.current_state != strategy.goal_state:
                print(f"The goal state {strategy.goal_state} is not reached",file=sys.stderr)

    # def validateStrategies(self):
    #     for strategy in self.strategies:
    #         self.transitionChecker(strategy)
    #
    # def transitionChecker(self, root: Strategy):
    #     supposedTransitionKind = 0
    #     for (child, action, isInput) in root.children:
    #         currentTransitionKind = 1 if isInput else -1
    #         if supposedTransitionKind == 0:
    #             supposedTransitionKind = currentTransitionKind
    #         elif supposedTransitionKind == 1:
    #             raise Exception(
    #                 "Multiple input transitions are possible from the same state")  # because I write code as if it always has 1 optimal way
    #         self.transitionChecker(child)

if __name__ == "__main__":
    specification = DummySpecification().fsm
    strategies = StrategySynthesiser(specification).synthesize_all_backward_induction()

    application = DummyApplication()
    test_executor = ExecuteTests(strategies, application,specification)
    test_executor.runTest()
