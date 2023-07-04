from functools import cached_property

from util import calculate_modifier

class PrimaryStat:
    def __init__(self, stat: int):
        self.stat = stat

    @property
    def stat(self) -> int:
        return self._stat

    @stat.setter
    def stat(self, stat: int):
        self._stat = stat

    @cached_property
    def modifier(self) -> int:
        return calculate_modifier(self.stat)

class PrimaryStatCollection:
    def __init__(
            self,
            strength: int,
            dexterity: int,
            constitution: int,
            intelligence: int,
            wisdom: int,
            charisma: int,
    ):
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma

    @property
    def charisma(self) -> PrimaryStat:
        return self._charisma

    @charisma.setter
    def charisma(self, charisma: int):
        self._charisma = charisma

    @property
    def wisdom(self) -> PrimaryStat:
        return self._wisdom

    @wisdom.setter
    def wisdom(self, wisdom: int):
        self._wisdom = PrimaryStat(wisdom)

    @property
    def intelligence(self) -> PrimaryStat:
        return self._intelligence

    @intelligence.setter
    def intelligence(self, intelligence: int):
        self._intelligence = PrimaryStat(intelligence)

    @property
    def constitution(self) -> PrimaryStat:
        return self._constitution

    @constitution.setter
    def constitution(self, constitution: int):
        self._constitution = PrimaryStat(constitution)

    @property
    def strength(self) -> PrimaryStat:
        return self._strength

    @strength.setter
    def strength(self, strength: int):
        self._strength = PrimaryStat(strength)

    @property
    def dexterity(self) -> PrimaryStat:
        return self._dexterity

    @dexterity.setter
    def dexterity(self, dexterity: int):
        self._dexterity = PrimaryStat(dexterity)



