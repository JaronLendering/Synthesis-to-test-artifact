import multiprocessing
import os

import select
import sys
import io
import threading

from application.automaton import Transition

class InputOutputProcessing:

    def __init__(self):
        self._input_queue_ = multiprocessing.Queue()
        self._output_queue_ = multiprocessing.Queue()
        self.input_process_lock = multiprocessing.Lock()

    def input_emulator(self,input):
        str_input = str(input)
        self._input_queue_.put(str_input)

    def input_dequeue(self):
        if self._input_queue_ is None:
            raise Exception("Input reading has not been started")
        self.input_process_lock.acquire()
        user_input = self._input_queue_.get()
        print(user_input + "?")
        self.input_process_lock.release()
        return user_input
    def output_emulator(self, text):
        self.input_process_lock.acquire()
        self._output_queue_.put(str(text))
        print(str(text) + "!")
        self.input_process_lock.release()
    def output_dequeue(self):
        if self._input_queue_ is None:
            raise Exception("Ouput reading has not been started")
        return self._output_queue_.get()

    def empty_queues(self):
        self._input_queue_ = multiprocessing.Queue()
        self._output_queue_ = multiprocessing.Queue()

def output_eager_assumpion_procesing(input_transition: Transition, output_transition: Transition) -> Transition:
    if str(output_transition.input_value) == "None" and str(input_transition.input_value) != "None":
        return input_transition
    else:
        return output_transition


def assumption_processing_transition(t1: Transition, t2: Transition) -> Transition:
    if t1.isInput == t2.isInput:
        raise Exception(f"{t1} and {t2} are both {'input' if t1.isInput else 'output'} transitions")
    if t1.isInput:
        return output_eager_assumpion_procesing(t1, t2)
    else:
        return output_eager_assumpion_procesing(t2, t1)

def assumption_processing_input_output(input, output):
    return output_eager_assumpion_procesing(Transition(input,None,True), Transition(output,None,False)) #the endstates don't matter