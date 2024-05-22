import sys
from threading import Condition

class catchStateChanges:

    def __init__(self,state_changed: Condition):
        self.print_queue = []
        self.state_changed = state_changed
        self._original_write_ = sys.stdout.write

    def catchPrintMessages(self):
        sys.stdout.write = self.newPrintMethod
    def newPrintMethod(self,text):
        self.print_queue.append(text)
        self.state_changed.notify_all()
        self._original_write_(text)

    def catchAllOutput(self):
        self.catchPrintMessages()


    def __del__(self):
        sys.stdout.write = self._original_write_

