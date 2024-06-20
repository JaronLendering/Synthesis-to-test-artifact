from application.automaton import State
from abc import ABC, abstractmethod


class Strategy(ABC):


    @abstractmethod
    def return_input(self,**args) -> str:
        pass
