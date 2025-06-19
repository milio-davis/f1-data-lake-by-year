-- 1. Top 10 drivers with the most race wins
SELECT 
    driverRef, 
    COUNT(*) AS wins
FROM f1_results
WHERE position = '1'
GROUP BY driverRef
ORDER BY wins DESC
LIMIT 10;

-- 2. Constructors with the most podium finishes
SELECT 
    constructorRef, 
    COUNT(*) AS podiums
FROM f1_results
WHERE position IN ('1', '2', '3')
GROUP BY constructorRef
ORDER BY podiums DESC
LIMIT 10;

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
    circuitRef, 
    COUNT(*) AS total_races
FROM f1_races
GROUP BY circuitRef
ORDER BY total_races DESC;

-- 5. Driver performance at a specific circuit (e.g., monza)
SELECT 
    r.year, 
    d.driverRef, 
    res.position
FROM f1_results res
JOIN f1_races r ON res.raceId = r.raceId
JOIN f1_drivers d ON res.driverId = d.driverId
WHERE r.circuitRef = 'monza'
ORDER BY r.year DESC, res.position;

-- 6. First race year for each driver
SELECT 
    driverRef,
    MIN(year) AS debut_year
FROM f1_results res
JOIN f1_races r ON res.raceId = r.raceId
GROUP BY driverRef
ORDER BY debut_year;
