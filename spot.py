from enum import Enum


class SPOT(Enum):
    RED = 0
    YELLOW = 1
    EMPTY = 2

    def __str__(self):
        if self.value == 0:
            return 'R'
        elif self.value == 1:
            return 'Y'
        else:
            return '_'

    def is_empty(self):
        return self.value == 2