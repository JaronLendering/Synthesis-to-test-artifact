from enum import Enum

from application.dummyApplication import DummyApplication
from application.goodApplication import GoodApplication


class SpecTypes(Enum):
    GOOD = GoodApplication
    DUMMY = DummyApplication
