import random
import sys
import multiprocessing
from typing import Callable
from application.catchStateChanges import catchStateChanges


class DummyApplication:
    def __init__(self):
        self.read_input = None

    def set_read_input(self, read_input: Callable[[],str]):
        self.read_input = read_input

    def read_input_set(self):
        if callable(self.read_input):
            raise Exception("input reading has not been started")
    def output(self,output):
        print(output)

    def startMusic(self):
        print("startMusic")

    def stopMusic(self):
        print("stopMusic")

    def finished(self):
        print("finished")

    def timeout(self):
        print("timeout")

    def run(self):
        self.read_input_set()
        print('give 0 for starting music and 1 for stopping music')
        self.read_input()
        output = None if random.random() < 0.5 else 'f'
        print(output)
        startNumber = self.read_input()
        if output == 'f':
            self.finished()
        else:
            if(startNumber == '0'):
                self.startMusic()
            elif(startNumber == '1'):
                self.stopMusic()
            else:
                self.timeout()



if __name__ == '__main__':
    app = DummyApplication()
    output_catcher = catchStateChanges()
    output_catcher.catchPrintMessages()
    app.run()
    print(output_catcher._print_queue_)