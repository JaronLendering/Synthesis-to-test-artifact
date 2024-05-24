import sys
import threading
from threading import Condition

class catchStateChanges:

    def __init__(self):
        self._print_queue_ = []
        self.state_changed = threading.Condition()
        self._original_write_ = sys.stdout.write

    def reset(self):
        self._print_queue_ = []
    def catchPrintMessages(self):
        sys.stdout.write = self.newPrintMethod
    def newPrintMethod(self,text):
        with self.state_changed:
            if text != "\n": # print autmatically adds a /n after every print
                self._print_queue_.append(text)
                self.state_changed.notify_all()
            self._original_write_(text)

    def catch_all_output(self):
        self.catchPrintMessages()


    def print_dequeue(self):
        with self.state_changed:
            if self._print_queue_ == []:
                self.state_changed.wait()
        output = self._print_queue_[0]
        self._print_queue_.remove(output)
        return output

    def __del__(self):
        sys.stdout.write = self._original_write_

