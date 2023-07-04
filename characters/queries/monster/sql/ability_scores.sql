SELECT
    str as strength, dex as dexterity, wis as wisdom,
    con as constitution, int as intelligence, cha as charisma
FROM monster
WHERE id=:id;