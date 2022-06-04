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
, year_agg AS (
SELECT 
    EXTRACT(year FROM release_date)   AS release_year
  , ROUND(AVG(profit_absolute), 0)    AS avg_profit_absolute
  , ROUND(AVG(profit_percentage), 2)  AS avg_profit_perc
FROM profits
GROUP BY EXTRACT(year FROM release_date)
)

, yoy_comparisons AS (
SELECT 
    release_year                                                AS release_year
  , avg_profit_perc                                             AS avg_profit_perc
  , LEAD(avg_profit_perc) OVER (ORDER BY release_year DESC)     AS avg_profit_perc_last_year
  , avg_profit_absolute                                         AS avg_profit_absolute
  , LEAD(avg_profit_absolute) OVER (ORDER BY release_year DESC) AS avg_profit_absolute_last_year
FROM year_agg
)

SELECT 
    release_year
  , avg_profit_perc
  , ROUND(
        (avg_profit_perc - avg_profit_perc_last_year)
        / avg_profit_perc_last_year
      , 2
   )          AS avg_profit_perc_growth_yoy
  , avg_profit_absolute
  , ROUND(
        (avg_profit_absolute - avg_profit_absolute_last_year)
        / avg_profit_absolute_last_year
      , 2
   )          AS avg_profit_absolute_growth_yoy
FROM yoy_comparisons
ORDER BY release_year DESC
