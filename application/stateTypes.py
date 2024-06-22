from enum import Enum


class StateTypes(Enum):
    OTHER = 0
    LINES = 1
    CHOICES = 2
    LOOP = 3
    START = 4