-- 1. Top 10 drivers with the most race wins
SELECT 
    res.driver_code, 
    COUNT(*) AS wins,
    res.season
FROM results res
LEFT JOIN drivers dr ON res.driver_code = dr.code AND res.season = dr.season
WHERE res.position = 1
GROUP BY res.driver_code, res.season
ORDER BY wins DESC
;

-- 2. Constructors with the most podium finishes
SELECT 
    con.name AS constructor_name, 
    COUNT(*) AS podiums,
    res.season
FROM results res
LEFT JOIN constructors con ON con.constructor_id = res.constructor_id AND res.season = con.season
WHERE position IN (1, 2, 3)
GROUP BY con.name, res.season
ORDER BY podiums DESC
;

-- 3. Average finish position by driver
SELECT 
    driverRef,
    AVG(CAST(position AS INT)) AS avg_finish
FROM f1_results
WHERE position != '\\N'  -- Filter out nulls or missing data
GROUP BY driverRef
ORDER BY avg_finish ASC
LIMIT 10;

-- 4. Number of races hosted by each circuit
SELECT 
    rc.name, 
    COUNT(*) AS total_races
FROM races rc
GROUP BY rc.name
ORDER BY total_races DESC
;

-- 5. Driver performance at a specific circuit
SELECT 
    res.season, 
    d.given_name, 
    res.position,
    r.race_name
FROM results res
JOIN races r ON res.race_round_id = r.round AND r.season = res.season
JOIN drivers d ON res.driver_code = d.code AND d.season = res.season
WHERE r.race_name = 'Australian Grand Prix'
ORDER BY r.season DESC, res.position
;
