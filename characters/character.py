from __future__ import annotations
from abc import abstractmethod, ABC
from enum import Enum, auto
from dataclasses import dataclass
from typing import Set

from util import calculate_modifier


@dataclass
class AbilityScore:
    value: int

    @property
    def modifier(self) -> int:
        return calculate_modifier(self.value)


class AbilityScores:

    def __init__(
            self,
            strength: int,
            dexterity: int,
            wisdom: int,
            constitution: int,
            intelligence: int,
            charisma: int
    ):
        self.strength = AbilityScore(strength)
        self.dexterity = AbilityScore(dexterity)
        self.wisdom = AbilityScore(wisdom)
        self.constitution = AbilityScore(constitution)
        self.intelligence = AbilityScore(intelligence)
        self.charisma = AbilityScore(charisma)

    def __eq__(self, other: AbilityScores):
        if not isinstance(other, AbilityScores):
            return False
        stri = self.strength == other.strength
        dex = self.dexterity == other.dexterity
        wis = self.wisdom == other.wisdom
        con = self.constitution == other.constitution
        inte = self.intelligence == other.intelligence
        cha = self.charisma == other.charisma
        return stri and dex and wis and con and inte and cha


@dataclass
class SavingThrows:
    strength: bool
    dexterity: bool
    wisdom: bool
    constitution: bool
    charisma: bool
    intelligence: bool


class Lawfulness(Enum):
    LAWFUL = "lawful"
    NEUTRAL = "neutral"
    CHAOTIC = "chaotic"


class Goodness(Enum):
    GOOD = "good"
    NEUTRAL = "neutral"
    EVIL = "evil"


@dataclass
class Alignment:
    lawfulness: Lawfulness
    goodness: Goodness


@dataclass
class Skills:
    acrobatics: int
    animal_handling: int
    arcana: int
    athletics: int
    deception: int
    history: int
    insight: int
    intimidation: int
    investigation: int
    medicine: int
    nature: int
    perception: int
    performance: int
    persuasion: int
    religion: int
    sleight_of_hand: int
    stealth: int
    survival: int


class Language(Enum):
    HUMAN = auto()
    GOBLIN = auto()
    # TODO: Add all other languages lol


@dataclass
class Languages:
    telepathic: bool
    languages: Set[Language]


class CharacterBuilder(ABC):

    @property
    @abstractmethod
    def character(self) -> ICharacter:
        pass

    @abstractmethod
    def build_meta(self) -> CharacterBuilder:
        self._character.meta_name = self.__class__.__name__
        return self

    @abstractmethod
    def build_physical_stats(self) -> CharacterBuilder:
        pass

    @abstractmethod
    def build_behaviours(self, alignment: Alignment) -> CharacterBuilder:
        self._character.alignment = alignment
        return self

    @abstractmethod
    def build_base_stats(self, base_stats: BaseStats) -> CharacterBuilder:
        self._character.base_stats = base_stats
        return self

    @abstractmethod
    def build_ability_scores(self, ability_scores: AbilityScores) -> CharacterBuilder:
        self._character.ability_scores = ability_scores
        return self

    @abstractmethod
    def build_saving_throws(self, saving_throws: SavingThrows) -> CharacterBuilder:
        self._character.saving_throws = saving_throws
        return self

    @abstractmethod
    def build_skills(self, skills: Skills) -> CharacterBuilder:
        self._character.skills = skills
        return self

    @abstractmethod
    def build_immunities(self, damage_modifiers: DamageModifiers) -> CharacterBuilder:
        self._character.damage_modifiers = damage_modifiers
        return self

    @abstractmethod
    def build_senses(self, senses: Senses) -> CharacterBuilder:
        self._character.senses = senses
        return self

    @abstractmethod
    def build_challenge(self) -> CharacterBuilder:
        pass

    @abstractmethod
    def build_language(self, languages: Languages) -> CharacterBuilder:
        self._character.languages = languages
        return self

    @abstractmethod
    def build_traits(self) -> CharacterBuilder:
        pass

    @abstractmethod
    def build_combat(self) -> CharacterBuilder:
        pass


class CharacterSize(Enum):
    TINY = "tiny"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    HUGE = "huge"
    GARGANTUAN = "gargantuan"


# class MonsterType(Enum):
#     # TODO: grab the types
#     ABERRATION = auto()
#     BEAST = auto()


@dataclass
class PhysicalStats:
    size: CharacterSize
    type: str
    tags: str


@dataclass
class Speed:
    walk: int
    burrow: int
    climb: int
    fly: int
    swim: int


@dataclass
class BaseStats:
    armor_class: int
    hit_points: int
    speed: Speed


class DamageType(Enum):
    ACID = auto()
    BLUDGEONING = auto()
    COLD = auto()
    FIRE = auto()
    FORCE = auto()
    LIGHTNING = auto()
    NECROTIC = auto()
    PIERCING = auto()
    POISON = auto()
    PSYCHIC = auto()
    RADIANT = auto()
    SLASHING = auto()
    THUNDER = auto()


@dataclass
class DamageModifiers:
    immunities: Set[DamageType]
    resistances: Set[DamageType]
    vulnerabilities: Set[DamageType]


class Sense(Enum):
    BLINDSIGHT = auto()
    DARKVISION = auto()
    TREMORSENSE = auto()
    TRUESIGHT = auto()


@dataclass
class Senses:
    passive_perception: int
    senses: Set[Sense]


@dataclass
class Challenge:
    challenge_rating: float

    @property
    def experience_value(self) -> int:
        run_sum = 0
        for i in range(1, self.challenge_rating):
            run_sum += (i + i // 7) * 100

        return run_sum + 100


class Trait(Enum):
    INNATE_SPELLCASTING = auto()
    SPELLCASTING = auto()
    PSIONICS = auto()


@dataclass
class Traits:
    traits: Set[Trait]


class NPCharacterBuilder(CharacterBuilder):

    def __init__(self):
        self.reset()

    def reset(self):
        self._character = NPCharacter()

    @property
    def character(self) -> NPCharacter:
        character = self._character
        self.reset()
        return character

    def build_physical_stats(self, stats: PhysicalStats) -> NPCharacterBuilder:
        self._character.physical_stats = stats
        return self

    def build_behaviours(self, alignment: Alignment) -> NPCharacterBuilder:
        return super().build_behaviours(alignment)

    def build_base_stats(self, base_stats: BaseStats) -> NPCharacterBuilder:
        return super().build_base_stats(base_stats)

    def build_ability_scores(self, ability_scores: AbilityScores) -> NPCharacterBuilder:
        return super().build_ability_scores(ability_scores)

    def build_saving_throws(self, saving_throws: SavingThrows) -> NPCharacterBuilder:
        return super().build_saving_throws(saving_throws)

    def build_skills(self, skills: Skills) -> NPCharacterBuilder:
        return super().build_skills(skills)

    def build_immunities(self, damage_modifiers: DamageModifiers) -> NPCharacterBuilder:
        return super().build_immunities(damage_modifiers)

    def build_senses(self, senses: Senses) -> NPCharacterBuilder:
        return super().build_senses(senses)

    def build_challenge(self, challenge_rating: Challenge) -> NPCharacterBuilder:
        self._character.challenge = challenge_rating
        return self

    def build_language(self, languages: Languages) -> NPCharacterBuilder:
        return super().build_language(languages)

    def build_traits(self, traits: Traits) -> NPCharacterBuilder:
        self._character.traits = traits
        return self

    def build_combat(self) -> NPCharacterBuilder:
        self._character.combat = "Oh god"
        return self

    def build_meta(self) -> NPCharacterBuilder:
        return super().build_meta()


@dataclass
class ICharacter(ABC):
    """
    Shared behaviour between player characters and non-playable characters
    go in this interface
    """
    physical_stats: PhysicalStats = None
    alignment: Alignment = None
    base_stats: BaseStats = None
    ability_scores: AbilityScores = None
    saving_throws: SavingThrows = None
    skills: Skills = None
    damage_modifiers: DamageModifiers = None
    passive_perception: int = None
    senses: Senses = None
    telepathic: bool = None
    languages: Languages = None
    traits: Traits = None
    combat: str = None


class NPCharacter(ICharacter):
    """
    Non-playable character behaviours go in this interface
    """
    challenge: Challenge = None


class PlayableCharacter(ICharacter):
    """
    Playable character behaviours go in this interface
    """
    pass


class CharacterDirector:
    """
    Character Director orchestrates creation of characters using all builder
    """

    def __init__(self):
        self._builder = None

    @property
    def builder(self) -> CharacterBuilder:
        return self._builder

    @builder.setter
    def builder(self, builder: CharacterBuilder) -> None:
        self._builder = builder

    def build_character(self, character_id: str) -> NPCharacter:
        pass
