
import inspect
import os
import time
from abc import abstractmethod, ABC

from matplotlib import pyplot as plt


from application.stateTypes import StateTypes
from strategy_synthesize_techniques import mctsTree, biStrategy
from strategy_synthesize_techniques.mctsTree import ActionChooserEnum
from strategy_synthesize_techniques.strategy import Strategy
from strategy_synthesize_techniques.strategySynthesizerEnum import StrategySynthesizerChooser
from strategy_synthesize_techniques.stratetegySynthesiser import StrategySynthesiser
from test_execution_files.applicationEndTypes import ApplicationEndTypes
from test_execution_files.executeTests import ExecuteTests

class SpecificationTests(ABC):
    def __init__(self, specification):
        self.specification = specification.fsm
        self.application = specification.type.value()
        self._data_folder_ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/")
        self.strategy_kind = None
        self.strategy_path: str = None
        self.synthesizer = None


    def create_path_in_data(self, path: str) -> str:
        return os.path.join(self._data_folder_, path)

    def termination_bargraph(self, dictionary):
        self.bargraph_dictionary(dictionary,f"{self.strategy_kind} Termination Factors","Termination Factors","Amount of Terminations","termination_factor",ApplicationEndTypes)

    def bargraph_dictionary(self,dictionary,title,category_label, value_label,folder,types_class):
        plt.figure(figsize=(14, 8))
        plt.bar([types_class(key).name for key in dictionary.keys()],
                list(dictionary.values()), color='skyblue')

        # Add title and labels
        plt.title(title)
        plt.xlabel(category_label)
        plt.ylabel(value_label)

        plt.tight_layout()
        path = os.path.join(self.strategy_path,folder)
        os.makedirs(path, exist_ok=True)
        plt.savefig(os.path.join(path,f"{ inspect.currentframe().f_back.f_back.f_back.f_code.co_name}.png"))

    def add_strategy_creation_time(self, strategy_creation_time):
        with open(os.path.join(self.strategy_path, "creation_time"), "a") as text_file:
            text_file.write(f"{inspect.currentframe().f_back.f_back.f_code.co_name}: {strategy_creation_time}\n")

    def add_win_rate_per_node_type(self, winning_strategies: [Strategy], strategies: [Strategy] ):
        type_exist_dict: {StateTypes,int} = {}
        type_win_dict: {StateTypes,float} = {}
        for winning_strategy in winning_strategies:
            type_win_dict.setdefault(winning_strategy.goal_state.type,0)
            type_win_dict.update({winning_strategy.goal_state.type: type_win_dict.get(winning_strategy.goal_state.type)+1})
        for strategy in strategies:
            type_exist_dict.setdefault(strategy.goal_state.type, 0)
            type_exist_dict.update({strategy.goal_state.type: type_exist_dict.get(strategy.goal_state.type) + 1})
        for key in type_win_dict.keys():
            type_win_dict.update({key: type_win_dict.get(key)/ type_exist_dict.get(key)})
        self.bargraph_dictionary(type_win_dict, f"{self.strategy_kind} Win Rate","Node Types","Win Amount","Win_Rates",StateTypes)

    def add_test_time(self, test_time):
        with open(os.path.join(self.strategy_path, "test_time"), "a") as text_file:
            text_file.write(f"{inspect.currentframe().f_back.f_back.f_code.co_name}: {test_time}\n")
        pass

    def test(self):
        current_time = time.time()
        strategies = self.synthesizer.strategy_synthesizer()
        strategy_creation_time = time.time() - current_time
        test_executor = ExecuteTests(strategies, self.application, self.specification)
        current_time = time.time()
        terminating_factors,winning_strategies = test_executor.runTest()
        test_time = time.time() - current_time
        self.add_strategy_creation_time(strategy_creation_time)
        self.add_win_rate_per_node_type(winning_strategies,strategies)
        self.add_test_time(test_time)
        self.extra_metrics(strategies)
        self.termination_bargraph(terminating_factors)

    @abstractmethod
    def extra_metrics(self, strategies):
        pass





class MctsTests(SpecificationTests):



    def __init__(self,  specification, show_strategies, SM_MCTS_version: ActionChooserEnum):
        super().__init__(specification)
        self.synthesizer = StrategySynthesiser(self.specification, StrategySynthesizerChooser.SM_MCST)
        self.synthesizer.action_chooser = SM_MCTS_version
        self.show_strategies = show_strategies
        self.strategy_path = self.create_path_in_data(f"MCTS/{SM_MCTS_version.name}")
        self.strategy_kind = "SM-MCTS"
        os.makedirs(os.path.join(self.strategy_path, "../"), exist_ok=True)
        os.makedirs(self.strategy_path,exist_ok=True)

    def extra_metrics(self, strategies: [mctsTree]):
        self.add_strategies_size(strategies)
        if self.show_strategies:
            self.add_strategy_graph(strategies)

    def add_strategies_size(self, strategies: [mctsTree]):
        with open(os.path.join(self.strategy_path, "mcts_strategy_graph_sizes"), "a") as text_file:
            text_file.write(f"{inspect.currentframe().f_back.f_back.f_back.f_code.co_name}\n\n")
            for strategy in strategies:
                text_file.write(f"\t{strategy.goal_state.name}: {len(strategy.transposition_table.keys())}\n")

    def add_strategy_graph(self, strategies: [mctsTree]):
        path = os.path.join(self.strategy_path, "MCTS_strategies")
        os.makedirs(path, exist_ok=True)
        for strategy in strategies:
            strategy.show(show=False,
                          given_path=os.path.join(path, inspect.currentframe().f_back.f_back.f_back.f_code.co_name))



class BiTests(SpecificationTests):


    def __init__(self, specification, show_strategies):
        super().__init__(specification)
        self.synthesizer = StrategySynthesiser(self.specification, StrategySynthesizerChooser.BI)
        self.show_strategies = show_strategies
        self.strategy_path = self.create_path_in_data("BI")
        self.strategy_kind = "BI"
        os.makedirs(self.strategy_path,exist_ok=True)

    def extra_metrics(self, strategies):
        if (self.show_strategies):
            self.add_strategy_table(strategies)
        self.add_strategy_node_space_sizes(strategies)
        pass


    def add_strategy_node_space_sizes(self, strategies: [biStrategy]):
        with open(os.path.join(self.strategy_path, "BI_node_space_sizes"), "a") as text_file:
            text_file.write(f"{inspect.currentframe().f_back.f_back.f_back.f_code.co_name}\n\n")
            for strategy in strategies:
                text_file.write(f"\t{strategy.goal_state.name}: {len(strategy.transitions.keys())}\n")

    def add_strategy_table(self, strategies: [biStrategy]):
        path = os.path.join(self.strategy_path, "BI_strategies")
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, inspect.currentframe().f_back.f_back.f_back.f_code.co_name), "a") as text_file:
            for strategy in strategies:
                text_file.write(f"{strategy.goal_state.name}\n")
                for state, transition in zip(strategy.transitions.keys(), strategy.transitions.values()):
                    text_file.write(f"\t{state}: {transition}\n")

