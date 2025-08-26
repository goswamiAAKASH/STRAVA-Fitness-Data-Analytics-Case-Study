select *from fitness_data;

select *from cleaned_master;

-- Average Steps per User
SELECT Id, ROUND(AVG(TotalSteps), 2) AS AvgSteps
FROM fitness_data
GROUP BY Id
ORDER BY AvgSteps DESC;

-- Sleep Efficiency (Sleep Minutes / Time in Bed)
SELECT Id, Date,
       ROUND(TotalMinutesAsleep * 1.0 / TotalTimeInBed, 2) AS SleepEfficiency
FROM fitness_data
WHERE TotalTimeInBed IS NOT NULL AND TotalMinutesAsleep IS NOT NULL;

-- Top 5 Most Active Users (By VeryActiveMinutes)
SELECT Id, SUM(VeryActiveMinutes) AS TotalVeryActiveMinutes
FROM fitness_data
GROUP BY Id
ORDER BY TotalVeryActiveMinutes DESC
LIMIT 5;

-- Average Steps vs Average Calories
SELECT 
    ROUND(AVG(TotalSteps), 2) AS AvgSteps,
    ROUND(AVG(Calories), 2) AS AvgCalories
FROM fitness_data;



-- Low Activity but High Sleep Days
SELECT Id, Date, TotalSteps, TotalMinutesAsleep
FROM fitness_data
WHERE TotalSteps < 5000 AND TotalMinutesAsleep > 400;

-- BMI Distribution
SELECT 
    ROUND(AVG(BMI), 2) AS AvgBMI,
    MIN(BMI) AS MinBMI,
    MAX(BMI) AS MaxBMI
FROM fitness_data
WHERE BMI IS NOT NULL;


select *from fitness_data;



