from abc import ABC, abstractmethod
from typing import Callable


class AbstractApplication(ABC):
    def __init__(self):
        self.read_input = None
        self.print_ouput = None

    def set_read_input(self, read_input: Callable[[], str]):
        self.read_input = read_input

    def set_print_output(self, print_output: Callable[[str], None]):
        self.print_ouput = print_output

    def read_input_set(self):
        if not callable(self.read_input):
            raise Exception("input reading has not been started")
    def do_IO_actions(self, output_func, state_changing_output_None = False):
        if not callable(output_func):
            raise Exception(
                "output is not a function. Output has to be a function to have the chance to change if output and input were None")

        while not state_changing_output_None:
            output = output_func()
            self.print_ouput(output)
            user_input = self.read_input()
            if user_input != "None" or output != "None":
                return user_input, output

        output = output_func()
        self.print_ouput(output)
        return self.read_input(), output

    @abstractmethod
    def run(self):
        pass