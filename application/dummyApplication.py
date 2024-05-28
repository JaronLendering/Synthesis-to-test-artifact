import random
import sys
import multiprocessing
from typing import Callable

from test_execution_files.InputOutputProcessing import InputOutputProcessing


class DummyApplication:
    def __init__(self):
        self.read_input = None
        self.print_ouput = None


    def set_read_input(self, read_input: Callable[[],str]):
        self.read_input = read_input

    def set_print_output(self, print_output: Callable[[str],None]):
        self.print_ouput = print_output


    def read_input_set(self):
        if not callable(self.read_input):
            raise Exception("input reading has not been started")
    def output(self,output):
        self.print_ouput(output)

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
        user_input,output = self.do_IO_actions("None")
        if user_input == "start":
            self.do_IO_actions('give 0 for starting music and 1 for stopping music')
            startNumber,output = self.do_IO_actions(None if random.random() < 0.5 else 'f')
            if output == 'f':
                self.finished()
            else:
                if(startNumber == '0'):
                    self.startMusic()
                elif(startNumber == '1'):
                    self.stopMusic()
                else:
                    self.timeout()
        elif user_input == "loop":
            while True:
                user_input, output = self.do_IO_actions(None if random.random() < 0.1 else 'L1')
                if output == 'L1':
                    self.do_IO_actions("L1 back")
                elif output == None:
                    if user_input == 'L2':
                        self.do_IO_actions("L2 back")



    def do_IO_actions(self, output):
        self.print_ouput(output)
        return self.read_input(),output



if __name__ == '__main__':
    app = DummyApplication()
    output_catcher = InputOutputProcessing()
    output_catcher.start_output_monitoring()
    app.run()
    print(output_catcher.output_dequeue())
    output_catcher.stop_output_monitoring()