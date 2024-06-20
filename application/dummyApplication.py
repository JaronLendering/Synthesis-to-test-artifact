import random
import sys
import multiprocessing
from typing import Callable

from application.abstractApplication import AbstractApplication
from test_execution_files.InputOutputProcessing import InputOutputProcessing


class DummyApplication(AbstractApplication):
    def startMusic(self):
        self.print_ouput("startMusic")

    def stopMusic(self):
        self.print_ouput("stopMusic")

    def finished(self):
        self.print_ouput("finished")

    def timeout(self):
        self.print_ouput("timeout")

    def run(self):
        self.read_input_set()
        user_input, output = self.do_IO_actions(lambda: "None")
        if user_input == "start":
            self.do_IO_actions(lambda: 'give 0 for starting music and 1 for stopping music')
            start_number, output = self.do_IO_actions(lambda: None if random.random() < 0.5 else 'f')
            if output == 'f':
                self.finished()
            else:
                if start_number == '0':
                    self.startMusic()
                elif start_number == '1':
                    self.stopMusic()
                else:
                    self.timeout()
        elif user_input == "loop":
            while True:
                user_input, output = self.do_IO_actions(lambda: None if random.random() < 0.1 else 'L1',True)
                if output == 'L1':
                    self.do_IO_actions(lambda: "L1 back")
                elif output == None:
                    if user_input == 'L2':
                        self.do_IO_actions(lambda: "L2 back")

