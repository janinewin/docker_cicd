-- This one should be failing for 29 records

SELECT 
    id 
  , COUNT(1) AS num_records
FROM movies_metadata
GROUP BY id
HAVING COUNT(1) > 1

-- More info about the duplicated records below
-- The duplication of the ID seems to regularly be coming from the fact that the popularity is differing
-- for the same ID
-- But it's not always the case - sometimes the 2 IDs have exactly the same information - they are pure duplicates

WITH duplicates AS (
SELECT 
    id 
  , COUNT(1) AS num_records
FROM movies_metadata
GROUP BY id
HAVING COUNT(1) > 1
)
SELECT *
FROM duplicates AS D
LEFT JOIN movies_metadata AS MM 
  ON D.id = MM.id
ORDER BY D.id
