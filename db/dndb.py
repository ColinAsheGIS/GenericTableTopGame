import os
import sqlite3

import pandas as pd

from util import ROOT_DIR

def get_connection() -> sqlite3.Connection:

    con = sqlite3.connect(os.path.join(ROOT_DIR, "db/monster.db"))

    def dict_factory(cursor, row):
        fields = [column[0] for column in cursor.description]
        return {key: value for key, value in zip(fields, row)}

    con.row_factory = dict_factory

    return con

def write_df_to_db(df: pd.DataFrame) -> None:

    con = get_connection()

    df.to_sql(
        name=df.attrs.get("table_name"),
        con=con,
        if_exists='replace'
    )

    con.commit()
    con.close()


def get_monster(id: int) -> None:
    conn = get_connection()

    cur = conn.cursor()

    res = cur.execute(
        "SELECT name FROM monster WHERE id=:id", {"id": id}
    )

    print(res.fetchone())
