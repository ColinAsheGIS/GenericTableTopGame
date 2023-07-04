from enum import Enum
import random

class Dice(Enum):
    d4 = 4
    d6 = 6
    d8 = 8
    d10 = 10
    d12 = 12
    d20 = 20
    d100 = 100

    def roll_die(self) -> int:
        return random.randint(1, self.value)
