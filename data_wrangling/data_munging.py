import re
import os

import pandas as pd

from db import write_df_to_db
from util import ROOT_DIR

def read_monster_workbook():
    df: pd.DataFrame = pd.read_excel(
        io=os.path.join(ROOT_DIR, 'resources/monster_excel.xlsx'),
        sheet_name="Official Stats",
        engine='openpyxl',
        dtype="string"
    )

    df = rename_monster_columns(df)
    df = transform_monster_size(df)
    df = transform_monster_type(df)
    df = transform_alignment(df)
    df = make_col_ints(df)
    df = create_speeds_table(df)
    df = create_skills_table(df)
    df = create_immunities_table(df)
    df = create_senses_table(df)
    df = create_saving_throws(df)
    df = create_languages_table(df)

    # Good to here marker

    df = df.drop(
        ["align", "font", "additional_info", "author"],
        axis='columns'
    )

    df = df.rename(columns={
        "monster_size": "size",
        "races": "tags"
    })

    df.attrs["table_name"] = "monster"

    write_df_to_db(df)

def create_languages_table(df: pd.DataFrame) -> pd.DataFrame:
    language_df = df.apply(
        lambda x: parse_language(x['languages']),
        axis='columns',
        result_type='expand'
    )
    language_df.index = language_df.index.rename('id')
    language_df["monster_id"] = language_df.index
    language_df.attrs["table_name"] = "language"
    write_df_to_db(language_df)
    df = df.drop(columns='languages')
    return df

def parse_language(input_str: str) -> dict:
    out_dict = {}
    try:
        input_str = input_str.split(",")
    except Exception:
        return out_dict

    word_regex = r"\w+[a-zA-Z]"

    for lang in input_str:
        finder = re.search(word_regex, lang)
        if finder:
            out_dict[finder.group(0).lower()] = 1
    return out_dict


def parse_saving_throws(input_str: str) -> dict:
    out_dict = {
        "str": 0,
        "dex": 0,
        "con": 0,
        "int": 0,
        "wis": 0,
        "cha": 0
    }

    try:
        input_str = input_str.lower()
    except AttributeError:
        return out_dict
    input_str = input_str.split(",")
    for saving_throw in input_str:
        val = saving_throw.strip()
        if val == "temp":
            continue
        out_dict[val] = 1
    return out_dict

def create_saving_throws(df: pd.DataFrame) -> pd.DataFrame:
    saving_throws = df.apply(
        lambda x: parse_saving_throws(x["sav_throws"]),
        axis='columns',
        result_type='expand'
    )
    saving_throws.index = saving_throws.index.rename('id')
    saving_throws["monster_id"] = saving_throws.index
    saving_throws.attrs["table_name"] = "saving_throw"
    write_df_to_db(saving_throws)
    df = df.drop(columns="sav_throws")
    return df

def parse_senses(input_str: str) -> dict:
    out_dict = {
        "darkvision": 0,
        "tremorsense": 0,
        "blindsight": 0,
        "truesight": 0
    }

    word_finder = r"\w+[a-zA-Z]"
    digit_finder = r"\w+[0-9]"
    senses = input_str.split(",")

    for sense in senses:
        word_group_found = re.search(word_finder, sense)
        digit_group_found = re.search(digit_finder, sense)
        if word_group_found:
            word_group = word_group_found.group(0).lower()

            match word_group:
                case "darkvision" | "darkivision":
                    key = "darkvision"
                case "blindsight":
                    key = "blindsight"
                case "truesight":
                    key = "truesight"
                case "tremorsense":
                    key = "tremorsense"
                case _:
                    continue
            if digit_group_found:
                out_dict[key] = int(digit_group_found.group(0))
    return out_dict

def create_senses_table(df: pd.DataFrame) -> pd.DataFrame:
    senses_df = df.apply(
        lambda x: parse_senses(x['senses']),
        axis='columns',
        result_type='expand'
    )
    senses_df.index = senses_df.index.rename('id')
    senses_df["monster_id"] = senses_df.index
    senses_df.attrs["table_name"] = "sense"
    write_df_to_db(senses_df)
    df = df.drop(columns="senses")
    return df

def create_immunities_table(df: pd.DataFrame) -> pd.DataFrame:
    immunities_df = df.apply(
        lambda x: generate_immunities_table(x['wri']),
        axis='columns',
        result_type='expand'
    )
    immunities_df.index = immunities_df.index.rename('id')
    immunities_df['monster_id'] = immunities_df.index
    immunities_df.attrs["table_name"] = "damage_mod"
    write_df_to_db(immunities_df)
    df = df.drop(columns="wri")
    return df

def make_col_ints(df: pd.DataFrame) -> pd.DataFrame:
    integer_cols = {
        "hp", "str", "dex", "con", "int",
        "wis", "cha", "ac"
    }
    for col in integer_cols:
        df[col] = df[col].apply(transform_int_val)
    return df

def rename_monster_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.index = df.index.rename("id")
    col: str
    for col in df.columns:
        new_col = col.replace(".", "").replace(" ", "_").lower()
        if new_col == "size":
            new_col = "monster_size"
        df = df.rename(
            columns={col: new_col}
        )
    return df

def generate_immunities_table(input_str: str) -> dict:
    output_dict = {
        "cold": None,
        "nonadamantine": None,
        "spell": None,
        "acid": None,
        "frightened grappled": None,
        "stunned": None,
        "charmed": None,
        "exhaustion": None,
        "thunder": None,
        "lightining": None,
        "grappled": None,
        "frightened": None,
        "unconscious": None,
        "paralyzed": None,
        "nonsilvered": None,
        "trainde": None,
        "deafened": None,
        "necrotic": None,
        "prone": None,
        "psychic": None,
        "darkness": None,
        "fire": None,
        "force": None,
        "magicalpiercing": None,
        "poisoned": None,
        "blinded": None,
        "slashing": None,
        "temp": None,
        "paralyezd": None,
        "poison": None,
        "nonsilvered ": None,
        "petrified": None,
        "magical": None,
        "pyschic": None,
        "exhuastion": None,
        "bludgeoning": None,
        "trained": None,
        "lightning": None,
        "piercing": None,
        "radiant": None,
        "nonmagical": None,
    }

    try:
        list_of_immuns = input_str.split(",")
    except Exception:
        return output_dict

    for damage_type in list_of_immuns:
        damage_type = damage_type.lower().strip()
        mods_regex = r"res|immun|weak|immmun|immu|immmu"
        try:
            subd = re.sub(mods_regex, "", damage_type)
            matching = re.search(mods_regex, damage_type)
            if subd in output_dict:
                match matching.group(0):
                    case 'res':
                        output_dict[subd] = 'resistance'
                    case 'immun' | 'immmun' | 'immu' | 'immmu':
                        output_dict[subd] = 'immunity'
                    case 'weak':
                        output_dict[subd] = 'weakness'
        except Exception:
            continue

    return output_dict

def generate_skills_table(input_str: str) -> dict:
    output_dict = {
        "intimidation": 0,
        "perception": 0,
        "investigation": 0,
        "acrobatics": 0,
        "animal_handling": 0,
        "religion": 0,
        "insight": 0,
        "survival": 0,
        "arcana": 0,
        "medicine": 0,
        "history": 0,
        "sleight_of_hand": 0,
        "innate_spellcasting": 0,
        "athletics": 0,
        "death_burst": 0,
        "nature": 0,
        "persuasion": 0,
        "stealth": 0,
        "performance": 0,
        "deception": 0,
    }

    try:
        skill_list = input_str.split(",")
    except AttributeError:
        return output_dict
    for skill in skill_list:
        if skill.lower().strip() in output_dict:
            if skill.lower().strip() == "intimation":
                skill = "intimidation"
            output_dict[skill.lower().strip().replace(" ", "_")] = 1
    return output_dict


def create_skills_table(df: pd.DataFrame) -> pd.DataFrame:
    skill_set = set()
    for skills in df['skills']:
        try:
            skill_list = skills.split(',')
        except Exception:
            continue
        for skill in skill_list:
            skill_set.add(skill.strip().lower())
    skill_set.remove('temp')
    skills_table = df.apply(
        lambda x: generate_skills_table(x["skills"]), axis='columns', result_type='expand'
    )
    skills_table["monster_id"] = skills_table.index
    skills_table.index = skills_table.index.rename("id")
    skills_table.attrs["table_name"] = "skills"
    write_df_to_db(skills_table)
    df = df.drop(columns='skills')
    return df

def transform_speeds(input_str: str) -> dict:
    out_dict = {
        "walk": 0,
        "swim": 0,
        "fly": 0,
        "climb": 0,
        "burrow": 0
    }
    try:
        speeds_list = input_str.split(",")
    except AttributeError:
        return out_dict

    word_finder = r"\w+[a-zA-Z]"
    digit_finder = r"\w+[0-9]"
    for speed_item in speeds_list:
        speed_finder = re.search(word_finder, speed_item)
        speed_type = "walk" if not speed_finder else speed_finder.group(0)
        if speed_type not in {'walk', 'swim', 'fly', 'climb', 'burrow'}:
            continue
        digit_found = re.search(digit_finder, speed_item)
        if digit_found:
            out_dict[speed_type] = int(digit_found.group(0))
        else:
            out_dict[speed_type] = 0
    return out_dict


def create_speeds_table(df: pd.DataFrame) -> pd.DataFrame:
    speeds_table = df.apply(lambda x: transform_speeds(x["speeds"]), axis='columns', result_type='expand')
    speeds_table.index = speeds_table.index.rename("id")
    speeds_table["monster_id"] = speeds_table.index
    speeds_table.attrs["table_name"] = "speed"
    write_df_to_db(speeds_table)
    df = df.drop(columns='speeds')
    return df

def transform_int_val(input_str: str) -> int:
    try:
        return int(input_str)
    except (ValueError, TypeError):
        return -1

def transform_alignment(df: pd.DataFrame) -> pd.DataFrame:
    df["align"] = df["align"].apply(str.lower)
    df["lawfulness"] = df["align"].apply(parse_lawfulness_str)
    df["goodness"] = df["align"].apply(parse_goodness_str)
    return df

def parse_goodness_str(input_str: str) -> str:
    def parse_standard(input_chars: str) -> str:
        match input_chars[1]:
            case "n":
                return "neutral"
            case "g":
                return "good"
            case "e":
                return "evil"

    def parse_any_or_not(input_chars: str) -> str:
        match input_chars.split(" ")[0]:
            case "any":
                match input_chars.split(" ")[1]:
                    case "good":
                        return "good"
                    case "evil":
                        return "evil"
                    case _:
                        return "good, neutral, evil"
            case "not":
                match input_chars.split(" ")[1]:
                    case "good":
                        return "neutral, evil"
                    case "neutral":
                        return "good, evil"
                    case "evil":
                        return "good, neutral"
                    case _:
                        return "good, neutral, evil"

    def parse_non_standard(input_chars: str) -> str:
        match input_chars:
            case "any":
                return "good, neutral, evil"
            case "cg or ne":
                return "good, evil"
            case "ng/ne":
                return "good, evil"
            case _:
                return parse_any_or_not(input_chars)

    match len(input_str):
        case 2:
            return parse_standard(input_str)
        case 1:
            return "unaligned"
        case _:
            return parse_non_standard(input_str)

def parse_lawfulness_str(input_str: str) -> str:

    def parse_standard(input_chars: str) -> str:
        match input_chars[0]:
            case "n":
                return "neutral"
            case "l":
                return "lawful"
            case "c":
                return "chaotic"
            case _:
                return ""

    def parse_any_or_not(input_chars: str) -> str:
        match input_chars.split(" ")[0]:
            case "any":
                match input_chars.split(" ")[1]:
                    case "chaotic":
                        return "chaotic"
                    case "lawful":
                        return "lawful"
                    case _:
                        return "chaotic, neutral, lawful"
            case "not":
                match input_chars.split(" ")[1]:
                    case "chaotic":
                        return "lawful, neutral"
                    case "lawful":
                        return "chaotic, neutral"
                    case _:
                        return "chaotic, neutral, lawful"

    def parse_non_standard(input_chars: str) -> str:
        match input_chars:
            case "any":
                return "chaotic, neutral, lawful"
            case "cg or ne":
                return "chaotic, neutral"
            case "ng/ne":
                return "neutral"
            case _:
                return parse_any_or_not(input_chars)

    match len(input_str):
        case 2:
            return parse_standard(input_str)
        case 1:
            return "unaligned"
        case _:
            return parse_non_standard(input_str)

def transform_monster_type(df: pd.DataFrame) -> pd.DataFrame:
    find_races_exp = r"\((.*?)\)"
    df["races"] = df["type"].apply(
        lambda x: re.findall(find_races_exp, x)
    )

    def races_to_str(input: list) -> str:
        try:
            return input[0].strip().lower()
        except IndexError:
            return ""

    df["races"] = df["races"].apply(races_to_str)

    def remove_races(input: str) -> str:
        return re.sub(find_races_exp, "", input).strip().lower()

    df["type"] = df["type"].apply(remove_races)

    return df


def transform_monster_size(df: pd.DataFrame) -> pd.DataFrame:
    df.monster_size = df.monster_size.apply(str.lower)
    df = df.loc[df.monster_size != 'varies']  # Drop these template items
    return df


def main():
    read_monster_workbook()


if __name__ == '__main__':
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    main()
