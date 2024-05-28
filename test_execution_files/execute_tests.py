import multiprocessing
import sys
import threading
import time

from application.dummyApplication import DummyApplication
from application.dummySpecification import DummySpecification
from application.specification_exception import SpecificationException
from strategy_synthesize_techniques.biStrategySynthesiser import BiStrategySynthesiser
from strategy_synthesize_techniques.strategy import Strategy
from application.automaton import FSM
from strategy_synthesize_techniques.stratetegySynthesiser import StrategySynthesiser
from test_execution_files.InputOutputProcessing import *
from colorama import init, Fore




class ExecuteTests():
    def __init__(self, strategies: [Strategy], application: DummyApplication, specification: FSM):
        self.strategies = strategies
        self.application = application
        self.specification = specification

        self.input_output_processing = InputOutputProcessing()
        init() # use colorama


    def runTest(self):
        self.application.set_read_input(self.input_output_processing.input_dequeue)
        self.application.set_print_output(self.input_output_processing.output_emulator)
        for strategy in self.strategies:
            application_process = multiprocessing.Process(target=self.application.run,daemon=True)
            application_process.start()
            self.traverse_strategy(strategy,max_duplicate_nodes=5)
            self.reset_variables(application_process)

        print("done")


    def reset_variables(self, application_process):
        self.specification.current_state = self.specification.initial_state
        self.input_output_processing.empty_queues()
        application_process.terminate()
        application_process.join()
        application_process.close()
        self.input_output_processing.input_process_lock.acquire(block = False)
        self.input_output_processing.input_process_lock.release()

    def traverse_strategy(self, strategy, max_node_dept = None, max_duplicate_nodes = None, node_dept = 0,
                          duplicate_node=None):

        if duplicate_node is None:
            duplicate_node = {}
        if self.specification.current_state == strategy.goal_state:
            print(f"{Fore.GREEN} The goal state {strategy.goal_state} is reached {Fore.RESET}")
            return
        if self.specification.current_state.is_terminal():
            print( f"The goal state {strategy.goal_state} is not reached. The state it is in now is {self.specification.current_state}",
                file=sys.stderr)
            return

        if max_node_dept != None:
            if node_dept > max_node_dept:
                print(f"Max node dept reached. Final state was {self.specification.current_state}",
                    file=sys.stderr)
        if max_duplicate_nodes != None:
            if max_duplicate_nodes <= duplicate_node.get(self.specification.current_state,0):
                print(f"Maximum amount of duplicates reached. {self.specification.current_state} is seen {duplicate_node.get(self.specification.current_state)+1} times",
                      file=sys.stderr)
                return

        self.input_output_processing.input_process_lock.acquire(block=False)
        self.input_output_processing.input_process_lock.release()

        node_dept += 1
        duplicate_node.update({self.specification.current_state: duplicate_node.get(self.specification.current_state,0) + 1})
        output = self.input_output_processing.output_dequeue()
        input = strategy.return_input(self.specification.current_state)
        transition = assumption_processing_input_output(input,output)
        try:
            self.specification.process_data(transition.input_value,transition.isInput)
        except SpecificationException as e:
            print(e.args[0],file=sys.stderr)

        self.input_output_processing.input_emulator(input)
        self.input_output_processing.input_process_lock.acquire()
        self.traverse_strategy(strategy,max_node_dept,max_duplicate_nodes,node_dept,duplicate_node)



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
    strategies = BiStrategySynthesiser(specification).synthesize_all_backward_induction()

    application = DummyApplication()
    test_executor = ExecuteTests(strategies, application,specification)
    test_executor.runTest()
