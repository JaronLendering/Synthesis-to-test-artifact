import argparse
import inspect
import os
import time
import subprocess
from abc import abstractmethod, ABCMeta, ABC
from threading import Thread

from matplotlib import pyplot as plt

from application.automaton import State, StateGenerator
from application.dummyApplication import DummyApplication
from application.dummySpecification import DummySpecification
from application.goodApplication import GoodApplication
from application.goodSpecification import GoodSpecification
from application.stateTypes import StateTypes
from strategy_synthesize_techniques import mctsTree, biStrategy
from strategy_synthesize_techniques.mctsTree import ActionChooserEnum
from strategy_synthesize_techniques.strategy import Strategy
from strategy_synthesize_techniques.strategySynthesizerEnum import StrategySynthesizerChooser
from strategy_synthesize_techniques.stratetegySynthesiser import StrategySynthesiser
from test_execution_files.applicationEndTypes import ApplicationEndTypes
from test_execution_files.executeTests import ExecuteTests
from test_execution_files.testClasses import BiTests, MctsTests


def dummy_test_test(show_strategies=False):
    dummy_BI_test()
    dummy_SM_MCTS_test(show_strategies)


def dummy_BI_test(show_strategies=False, action_chooser=None):
    tester = BiTests(DummySpecification(),show_strategies)
    tester.test()

def dummy_SM_MCTS_test(show_strategies=False, action_chooser=ActionChooserEnum.RANDOM):
    tester = MctsTests(DummySpecification(), show_strategies,action_chooser)
    tester.test()


def basic_BI_test(show_strategies=False, action_chooser=None):
    tester = BiTests(GoodSpecification(), show_strategies)
    tester.test()

def basic_SM_MCTS_test(show_strategies=False, action_chooser=ActionChooserEnum.RANDOM):
    tester = MctsTests(GoodSpecification(), show_strategies,action_chooser)
    tester.test()


def high_value_SM_MCTS_test(show_strategies=False, action_chooser=ActionChooserEnum.RANDOM):
    tester = MctsTests(GoodSpecification(), show_strategies, action_chooser)
    tester.synthesizer.set_MCTS_configuration_values(max_select_recursion=150, max_rollout_recursion=300)
    tester.test()


def high_iteration_SM_MCTS_test(show_strategies=False, action_chooser=ActionChooserEnum.RANDOM):
    tester = MctsTests(GoodSpecification(), show_strategies, action_chooser)
    tester.synthesizer.set_MCTS_configuration_values(iteration_count=300)
    tester.test()


def high_value_medium_iteration_SM_MCTS_test(show_strategies=False, action_chooser=ActionChooserEnum.RANDOM):
    tester = MctsTests(GoodSpecification(), show_strategies, action_chooser)
    tester.synthesizer.set_MCTS_configuration_values(iteration_count=200, max_select_recursion=150, max_rollout_recursion=300)
    tester.test()


def high_iter_SM_MCTS_lines_test(show_strategies=False, action_chooser=ActionChooserEnum.RANDOM):
    tester = MctsTests(GoodSpecification(lines=True), show_strategies, action_chooser)
    tester.synthesizer.set_MCTS_configuration_values(iteration_count=300)
    tester.test()


def high_iter_SM_MCTS_choices_test(show_strategies=False, action_chooser=ActionChooserEnum.RANDOM):

    tester = MctsTests(GoodSpecification(choices=True), show_strategies, action_chooser)
    tester.synthesizer.set_MCTS_configuration_values(iteration_count=300)
    tester.test()


def high_iter_SM_MCTS_loop_test(show_strategies=False, action_chooser=ActionChooserEnum.RANDOM):
    tester = MctsTests(GoodSpecification(loop=True), show_strategies, action_chooser)
    tester.synthesizer.set_MCTS_configuration_values(iteration_count=300)
    tester.test()

def BI_lines_test(show_strategies=False, action_chooser=None):
    tester = BiTests(GoodSpecification(lines=True), show_strategies)
    tester.test()



def BI_choices_test(show_strategies=False, action_chooser=None):
    tester = BiTests(GoodSpecification(choices=True), show_strategies)
    tester.test()


def BI_loop_test(show_strategies=False, action_chooser=None):
    tester = BiTests(GoodSpecification(loop=True), show_strategies)
    tester.test()


def high_value_hundered_iterations_SM_MCTS_loop_lines(show_strategies=False, action_chooser=ActionChooserEnum.RANDOM):
    tester = MctsTests(GoodSpecification(loop=True,lines=True), show_strategies, action_chooser)
    tester.synthesizer.set_MCTS_configuration_values(iteration_count=100, max_select_recursion=150, max_rollout_recursion=300)
    tester.test()

def medium_value_hundered_iterations_SM_MCTS_testing(show_strategies=False, action_chooser=ActionChooserEnum.RANDOM):
    tester = MctsTests(GoodSpecification(), show_strategies, action_chooser)
    tester.synthesizer.set_MCTS_configuration_values(iteration_count=100, max_select_recursion=150,
                                                     max_rollout_recursion=300)
    tester.test()


if __name__ == '__main__':
    # threads don't work properly with the application, because it is created with a new process. That is why it is most efficient to
    # just start multiple instances, all with different tests.
    parser = argparse.ArgumentParser()

    # Add arguments
    parser.add_argument('test_index', type=int, help='Index of the test to run.')
    parser.add_argument('--save_strategy', action='store_true', help='strategies have to be saved.')
    parser.add_argument('--better_MCTS', action='store_true', help='strategies have to be saved.')

    args = parser.parse_args()
    action_chooser = ActionChooserEnum.RANDOM
    if args.better_MCTS:
        action_chooser = ActionChooserEnum.NO_NONE

    tests = [BI_loop_test,
             BI_choices_test,
             BI_lines_test,
             high_iter_SM_MCTS_loop_test,
             high_iter_SM_MCTS_choices_test,
             high_iter_SM_MCTS_lines_test,
             high_iteration_SM_MCTS_test,
             high_value_SM_MCTS_test,
             basic_SM_MCTS_test,
             basic_BI_test,
             high_value_medium_iteration_SM_MCTS_test,
             high_value_hundered_iterations_SM_MCTS_loop_lines,
             medium_value_hundered_iterations_SM_MCTS_testing]

    chosen_test = tests[args.test_index]
    print(chosen_test.__name__)
    chosen_test(args.save_strategy, action_chooser)
    #basic_BI_test(True)
    exit(880)

