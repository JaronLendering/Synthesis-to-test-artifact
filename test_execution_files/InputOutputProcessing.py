import multiprocessing
import os

import select
import sys
import io
import threading

from application.automaton import Transition

class InputOutputProcessing:

    def __init__(self):
        self._input_queue_ = []
        self._input_condition_ = None
        self._terminate_cmd_monitoring_event = threading.Event()
        self._cmd_monitoring_thread= None
        self.normal_stdin = sys.stdin

    def cmd_set_input_mock(self):
        sys.stdin = io.StringIO()

    def cmd_reset_input_mock(self):
        sys.stdin = self.normal_stdin
    def cmd_input_emulator(self,input):
        sys.stdin.write(str(input))
    def start_cmd_monitoring(self):
        self._input_condition_ = threading.Condition()
        self._cmd_monitoring_thread = threading.Thread(target=self.__cmd_monitoring__,daemon=True)

    def stop_cmd_monitoring(self):
        if self._cmd_monitoring_thread is not None:
            self._terminate_cmd_monitoring_event.set()
            self._cmd_monitoring_thread.join()
            self._terminate_cmd_monitoring_event.clear()
        self._input_condition_ = None
    def __cmd_monitoring__(self):
        while not self._terminate_cmd_monitoring_event.is_set():
            if(sys.stdin.tell() < sys.stdin.seek(0,os.SEEK_END)):
                line = sys.stdin.readline().strip()
                with self._input_condition_:
                    self._input_queue_.append(line)
                    self._input_condition_.notify_all()

    def start_input_output_monitoring(self):
        self.start_cmd_monitoring()
        self.cmd_set_input_mock()

    def stop_input_output_monitoring(self):
        self.stop_cmd_monitoring()
        self.cmd_reset_input_mock()
    def input_dequeue(self):
        if self._input_condition_ is None:
            raise Exception("Input reading has not been started")
        with self._input_condition_:
            if self._input_queue_ == []:
                self._input_condition_.wait()
        input = self._input_queue_[0]
        self._input_queue_.remove(input)
        return input

def output_eager_assumpion_procesing(input_transition: Transition, output_transition: Transition) -> Transition:
    if output_transition.input_value == str(None) and input_transition.input_value is not None:
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