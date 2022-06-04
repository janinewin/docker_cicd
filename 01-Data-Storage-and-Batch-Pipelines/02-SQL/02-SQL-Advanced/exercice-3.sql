WITH profits AS (
SELECT 
    id
  , original_title
  , release_date
  , revenue 
  , budget
  , revenue - budget                        AS profit_absolute
  , ROUND((revenue - budget) / budget, 2)   AS profit_percentage
FROM movies_metadata
WHERE budget > 100000
AND revenue > 100000
)

SELECT 
    EXTRACT(year FROM release_date)   AS release_year
  , ROUND(AVG(profit_absolute), 0)    AS avg_profit_absolute
  , ROUND(AVG(profit_percentage), 2)  AS avg_profit_perc
FROM profits
GROUP BY EXTRACT(year FROM release_date)
ORDER BY EXTRACT(year FROM release_date) DESC
