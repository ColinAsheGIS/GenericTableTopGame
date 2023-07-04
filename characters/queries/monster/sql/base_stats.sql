SELECT
    m.ac as armor_class, m.hp as hit_points,
    speed.burrow as burrow, speed.walk as walk,
    speed.fly as fly, speed.climb as climb,
    speed.swim as swim
FROM monster as m
INNER JOIN main.speed speed on m.id = speed.monster_id
WHERE m.id=:id;
