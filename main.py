
from typing import Type, TypeVar
from enum import Enum
from characters.character import (
    Alignment, BaseStats, CharacterSize, Lawfulness, PhysicalStats, PlayableCharacterBuilder,
    Goodness, Speed
)

G = TypeVar('G', str, int, float)
E = TypeVar('E', bound=Enum)

def select_unbound_property(prop_name: str, prop_type: Type[G]) -> G:
    cast_type = None
    while cast_type is None:
        input_str = input(f"Select {prop_name}: ")
        try:
            cast_type = prop_type(input_str)
        except Exception:
            print(f"Invalid input for {prop_name} | [{prop_type}] can't be cast from {input_str}")
    return cast_type

def select_from_enum(cls: Type[E]) -> E:
    while (selection := input(f"Select {cls.__name__}: ").lower()) not in set(x.value for x in cls):
        print("Select From: ", end="\n\t")
        print('\n\t'.join([x.name.title() for x in cls]))
    return cls(selection)

def alignment_prompt() -> Alignment:
    return Alignment(
        lawfulness=select_from_enum(Lawfulness),
        goodness=select_from_enum(Goodness)
    )

def physical_stats_prompt() -> PhysicalStats:
    return PhysicalStats(
        size=select_from_enum(CharacterSize),
        type=select_unbound_property("Type", str),
        tags=select_unbound_property("Tags", str)
    )

def speed_prompt() -> Speed:
    return Speed(
        walk=select_unbound_property("Walk", int),
        burrow=select_unbound_property("Burrow", int),
        climb=select_unbound_property("Climb", int),
        fly=select_unbound_property("Fly", int),
        swim=select_unbound_property("Swim", int)
    )
def base_stats_prompt() -> BaseStats:
    return BaseStats(
        armor_class=select_unbound_property("Armor Class", int),
        hit_points=select_unbound_property("Hit Points", int),
        speed=speed_prompt()
    )


def main():
    """
    Build player character script
    """
    pc_builder = PlayableCharacterBuilder()

    physical_stats = physical_stats_prompt()
    print(physical_stats)

    behaviours = alignment_prompt()
    print(behaviours)

    base_stats = base_stats_prompt()
    print(base_stats)


if __name__ == "__main__":
    main()
