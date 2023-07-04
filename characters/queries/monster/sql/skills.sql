SELECT
    intimidation, perception,
    investigation, acrobatics, animal_handling,
    religion, insight, survival, arcana, medicine,
    history, sleight_of_hand,
    athletics, nature, persuasion,
    stealth, performance, deception
FROM skills
WHERE monster_id=:id;