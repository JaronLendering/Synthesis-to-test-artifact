import os
import random

import networkx as nx
from pyvis.network import Network

from application.automaton import State, Transition, FSM
from strategy_synthesize_techniques.strategy import Strategy
from test_execution_files.InputOutputProcessing import assumption_processing_transition


class MctsTree(Strategy):
    def __init__(self,winning_state,state:State, transposition_table,  specification_automaton):
        if transposition_table is None:
            transposition_table = {}
        self.goal_state = winning_state
        self.transposition_table = transposition_table
        self.specification_automaton = specification_automaton
        self.state = state
        self.score = 0
        self.action_score = {}
        self.visit_count = 0
        self.visits_action_count = {}
        self.unchecked_transitions = self.couple_transitions(state.input_transitions,state.output_transitions)

    def couple_transitions(self,inputs, outputs):
        coupled_transitions = {}

        for input in inputs:
            new_outputs = []
            for output in outputs:
                new_outputs.append(output) # to make the lists different so I can remove things from new_outputs without doing that to outputs
            coupled_transitions.update({input: new_outputs})
        return coupled_transitions


    def create_child(self, state):
        child = MctsTree(self.goal_state, state, self.transposition_table, self.specification_automaton)
        self.transposition_table.update({state:child})
        return child


    def increment_visited(self):
        self.visit_count += 1
        pass

    def increment_score(self, score):
        self.score += score
        pass

    def return_input(self,state:State) -> str|None:
        if state == self.state:
            input_action_and_score = ([Transition(None, self.state, True)], None)
            if self.action_score.keys():
                for action in self.action_score.keys():
                    if action in self.state.input_transitions:
                        score = self.action_score.get(action) / self.visits_action_count.get(action)
                        if input_action_and_score[1] is None or input_action_and_score[1] < score:
                            input_action_and_score = ([action], score)
                        elif input_action_and_score[1] == score:
                            input_action_and_score[0].append(action)
                return random.choices(input_action_and_score[0])[0].input_value
        elif self.transposition_table.get(state) is not None:
            return str(self.transposition_table[state].return_input(state))

        return None


    def summon_child(self, state):
        if state in self.transposition_table.keys():
            return self.transposition_table.get(state)
        return self.create_child(state)


    def increment_action_visited(self, action):
        current_count = self.visits_action_count.get(action,0)
        self.visits_action_count.update({action:current_count+1})


    def increment_action_score(self, score, action):
        current_count = self.action_score.get(action, 0)
        self.action_score.update({action: current_count + score})

    def get_unchecked_transition(self):
        if len(self.unchecked_transitions.keys()) > 0:
            input_trans,outputs = self.unchecked_transitions.popitem()
            output = outputs.pop()
            if outputs:
                self.unchecked_transitions.update({ input_trans:outputs})
            return input_trans, output
        return None

    def regret_update(self, test_action, tested_action, score):
        pass

    def regret_select(self):
        pass
    def duct_update(self, test_action, tested_action, score):
        self.increment_action_visited(test_action)
        self.increment_action_visited(tested_action)
        self.increment_action_score(score,test_action)
        self.increment_action_score(score,tested_action)

    def duct_select(self):
        input_action_and_score = ([Transition(None, self.state, True)], None)
        for action in self.state.input_transitions:
            score = self.action_score.get(action) / self.visits_action_count.get(action)
            if input_action_and_score[1] is None or input_action_and_score[1] < score:
                input_action_and_score = ([action], score)
            elif input_action_and_score[1] == score:
                input_action_and_score[0].append(action)

        chosen_input = random.choices(input_action_and_score[0])[0]
        output_action_and_score = ([Transition(None, self.state, False)], None)
        for action in self.state.output_transitions:
            score = self.action_score.get(action) / self.visits_action_count.get(action)
            if output_action_and_score[1] is None or output_action_and_score[1] < score:
                output_action_and_score = ([action], score)
            elif output_action_and_score[1] == score:
                output_action_and_score[0].append(action)
        chosen_output = random.choices(output_action_and_score[0])[0]

        return chosen_input,chosen_output

    def rollout(self, specification_automaton,max_rollout_iterations):
        new_state = self.state
        i = 0
        while not (self.state.is_terminal() or self.state.is_winning or max_rollout_iterations >= i):
            i+=1
            output_action,input_action = (random.choices(new_state.output_transitions)[0],random.choices(new_state.input_transitions)[0])
            transition = assumption_processing_transition(input_action, output_action)
            new_state = specification_automaton.process_data_from_state(new_state, transition.input_value,
                                                                             transition.isInput)
        return new_state.get_score()


    def show(self, net = None, seen_states=None):
        root = False
        if seen_states is None:
            root = True
            seen_states = []
        if self.state not in seen_states:
            seen_states.append(self.state)
            if net is None:
                net = Network(notebook=False, cdn_resources="remote",
                              bgcolor="#222222",
                              font_color="white",
                              height="750px",
                              width="100%",
                              directed=True
                              )
                net.force_atlas_2based(gravity=-273, central_gravity=0.015, spring_length=500)
                for state in self.specification_automaton.states:
                    net.add_node(str(state))
            input_actions = []
            output_actions = []
            for action in self.action_score.keys():
                if action in self.state.input_transitions:
                    input_actions.append(action)
                else:
                    output_actions.append(action)

            for input_trans in input_actions:
                for output_trans in output_actions:
                    transition = assumption_processing_transition(input_trans,output_trans)
                    end_state = self.specification_automaton.process_data_from_state(self.state,transition.input_value,transition.isInput)
                    net.add_edge(str(self.state), str(end_state), label=f"{input_trans}-{self.action_score.get(input_trans)/self.visits_action_count.get(input_trans)}-{output_trans}")
                    if self.transposition_table.get(end_state) is not None:
                        self.transposition_table[end_state].show(net,seen_states)
            if root:
                net.set_edge_smooth("dynamic")
                net.show(os.path.join("../data", f"mcts_tree_{self.goal_state}.html"), notebook=False)

