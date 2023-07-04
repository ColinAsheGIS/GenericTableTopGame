SELECT
    str as strength, dex as dexterity,
    wis as wisdom, con as constitution,
    cha as charisma, int as intelligence
FROM saving_throw
WHERE monster_id=:id;