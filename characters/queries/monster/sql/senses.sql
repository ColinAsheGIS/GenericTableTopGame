SELECT
    s.darkvision as darkvision, s.tremorsense as tremorsense,
    s.blindsight as blindsight, s.truesight as truesight,
    m.wis as passive_perception
FROM monster m INNER JOIN main.sense s on m.id = s.monster_id
WHERE m.id=340;