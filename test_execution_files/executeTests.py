import multiprocessing
import sys
import threading
import time

from application.abstractApplication import AbstractApplication
from application.dummyApplication import DummyApplication
from application.dummySpecification import DummySpecification
from application.goodApplication import GoodApplication
from application.goodSpecification import GoodSpecification
from application.specification_exception import SpecificationException
from strategy_synthesize_techniques import strategy

from strategy_synthesize_techniques.biStrategy import BiStrategy
from application.automaton import FSM
from strategy_synthesize_techniques.stratetegySynthesiser import StrategySynthesiser
from test_execution_files.InputOutputProcessing import *
from colorama import init, Fore

from test_execution_files.applicationEndTypes import ApplicationEndTypes
import matplotlib.pyplot as plt
class ExecuteTests():
    def __init__(self, strategies: [strategy], application: AbstractApplication, specification: FSM):
        self.strategies = strategies
        self.application = application
        self.specification = specification
        self.stop_kind_dictionary = {stop_kind: 0 for stop_kind in ApplicationEndTypes}
        self.input_output_processing = InputOutputProcessing()

        init() # use colorama


    def runTest(self):
        self.application.set_read_input(self.input_output_processing.input_dequeue)
        self.application.set_print_output(self.input_output_processing.output_emulator)
        winning_strategies = []
        for strategy in self.strategies:
            application_process = multiprocessing.Process(target=self.application.run,daemon=True)
            application_process.start()
            print(f"\t{strategy.goal_state}\n")
            message, stop_kind = self.traverse_strategy(strategy,max_duplicate_nodes=5)
            current_stop_number = self.stop_kind_dictionary.get(stop_kind)
            self.stop_kind_dictionary.update({stop_kind: current_stop_number+1})
            if stop_kind == ApplicationEndTypes.WIN:
                winning_strategies.append(strategy)
                print(f"{Fore.GREEN} \t{message}\n {Fore.RESET}")
            else:
                print(f"\t{message}\n", file = sys.stderr)

            self.reset_variables(application_process)
        print("done")
        return self.stop_kind_dictionary,winning_strategies


    def reset_variables(self, application_process):
        self.specification.current_state = self.specification.initial_state
        self.input_output_processing.empty_queues()
        if application_process.is_alive():
            application_process.terminate()
        application_process.join()
        application_process.close()
        self.input_output_processing.input_process_lock.acquire(block = False)
        self.input_output_processing.input_process_lock.release()

    def traverse_strategy(self, strategy, max_node_dept = None, max_duplicate_nodes = None, node_dept = 0,
                          duplicate_node=None) -> ():

        if duplicate_node is None:
            duplicate_node = {}
        if self.specification.current_state == strategy.goal_state:
            return (f"The goal state {strategy.goal_state} is reached", ApplicationEndTypes.WIN)

        if self.specification.current_state.is_terminal():
            return( f"The goal state {strategy.goal_state} is not reached. The state it is in now is {self.specification.current_state}",
                ApplicationEndTypes.TERMINAL)


        if max_node_dept != None: #was not necesarry in the end, was always kept as None
            if node_dept > max_node_dept:
                return(f"Max node dept reached. Final state was {self.specification.current_state}",
                    ApplicationEndTypes.MAX_NODE_DEPT)

        if max_duplicate_nodes != None:
            if max_duplicate_nodes <= duplicate_node.get(self.specification.current_state,0):
                return (f"Maximum amount of duplicates reached. {self.specification.current_state} is seen {duplicate_node.get(self.specification.current_state)+1} times",
                      ApplicationEndTypes.MAX_DUPLICATE_NODES)


        self.input_output_processing.input_process_lock.acquire(block=False)
        self.input_output_processing.input_process_lock.release()

        node_dept += 1
        duplicate_node.update({self.specification.current_state: duplicate_node.get(self.specification.current_state,0) + 1})
        output = self.input_output_processing.output_dequeue()
        input = strategy.return_input(self.specification.current_state)
        if input == None:
            return (f"The strategy couldn't reach the goal state {strategy.goal_state}. The strategy couldn't calculate further than state {self.specification.current_state}",
                ApplicationEndTypes.INCOMPLETE_STRATEGY)
        transition = assumption_processing_input_output(input,output)
        try:
            self.specification.process_data(transition.input_value,transition.isInput)
        except SpecificationException as e:
            return (e.args[0],ApplicationEndTypes.ILLEGAL_MOVE)


        self.input_output_processing.input_emulator(input)
        self.input_output_processing.input_process_lock.acquire()

        return self.traverse_strategy(strategy,max_node_dept,max_duplicate_nodes,node_dept,duplicate_node)



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
    specification = GoodSpecification().fsm
    strategies = StrategySynthesiser(specification,"BI").strategy_synthesizer()

    application = GoodApplication()
    test_executor = ExecuteTests(strategies, application,specification)
    test_executor.runTest()
