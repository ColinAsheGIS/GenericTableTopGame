import os

import util
from db import get_connection

from characters import PhysicalStats, Alignment, BaseStats, Speed, AbilityScores, SavingThrows, Skills, DamageModifiers, \
    Senses

conn = get_connection()

def get_statement(filename: str) -> str:
    cur_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '.'))
    cur_path = os.path.join(cur_dir, f"sql/{filename}")
    return open(cur_path, "r").read()

def physical_stats_by_id(id: int) -> PhysicalStats:
    cur = conn.cursor()
    statement = get_statement("physical_stats.sql")
    res = cur.execute(
        statement, {"id": id}
    )
    stats = PhysicalStats(**res.fetchone())
    cur.close()
    return stats

def alignment_by_id(id: int) -> Alignment:
    cur = conn.cursor()
    statement = get_statement("alignment.sql")
    res = cur.execute(
        statement, {"id": id}
    )
    stats = Alignment(**res.fetchone())
    cur.close()
    return stats

def base_stats_by_id(id: int) -> BaseStats:
    cur = conn.cursor()
    statement = get_statement("base_stats.sql")
    res = cur.execute(
        statement, {"id": id}
    )
    res = res.fetchone()
    base_stats = BaseStats(
        armor_class=res.get("armor_class"),
        hit_points=res.get("hit_points"),
        speed=Speed(
            burrow=res.get("burrow"),
            climb=res.get("climb"),
            fly=res.get("fly"),
            swim=res.get("swim"),
            walk=res.get("walk")
        )
    )
    cur.close()
    return base_stats

def ability_scores_by_id(id: int) -> AbilityScores:
    cur = conn.cursor()
    statement = get_statement("ability_scores.sql")
    res = cur.execute(
        statement, {"id": id}
    )
    stats = AbilityScores(**res.fetchone())
    cur.close()
    return stats

def saving_throws_by_id(id: int) -> SavingThrows:
    cur = conn.cursor()
    statement = get_statement("saving_throws.sql")
    res = cur.execute(
        statement, {"id": id}
    )
    int_dict = res.fetchone()
    for key, value in int_dict.items():
        int_dict[key] = bool(value)
    stats = SavingThrows(**int_dict)
    cur.close()
    return stats

def skills_by_id(id: int) -> Skills:
    cur = conn.cursor()
    statement = get_statement("skills.sql")
    res = cur.execute(
        statement, {"id": id}
    )
    skills_dict: dict = res.fetchone()
    stats = Skills(**skills_dict)
    cur.close()
    return stats

def immunities_by_id(id: int) -> DamageModifiers:
    cur = conn.cursor()
    statement = get_statement("immunities.sql")
    res = cur.execute(
        statement, {"id": id}
    )
    immunities_dict: dict = res.fetchone()
    # Each key in sql is a damage type, need each key to be a
    # resistance level instead
    mod_dict = {
        "immunities": set(),
        "resistances": set(),
        "vulnerabilities": set()
    }
    for key, value in immunities_dict.items():
        match value:
            case "immunity":
                mod_dict["immunities"].add(key)
            case "resistance":
                mod_dict["resistances"].add(key)
            case "weak":
                mod_dict["vulnerabilities"].add(key)
            case _:
                pass
    cur.close()
    return DamageModifiers(**mod_dict)

def senses_by_id(id: int) -> Senses:
    cur = conn.cursor()
    statement = get_statement("senses.sql")
    res = cur.execute(
        statement, {"id": id}
    )
    sense_dict = res.fetchone()
    out_dict = {
        "passive_perception": 0,
        "senses": set()
    }
    for key, value in sense_dict.items():
        match key:
            case "passive_perception":
                out_dict["passive_perception"] = util.calculate_modifier(value)
            case _:
                if value != 0:
                    out_dict["senses"].add(key)
    cur.close()
    return Senses(**out_dict)
