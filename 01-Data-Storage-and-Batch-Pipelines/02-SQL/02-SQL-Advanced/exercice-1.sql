SELECT
    SUM(
      CASE WHEN NULLIF(budget, 0) IS NULL OR NULLIF(budget, 0) IS NULL THEN 1
      ELSE 0
      END
    )                   AS num_records_null
  , COUNT(1)            AS num_records_total
  , ROUND(
    CAST(SUM(
      CASE WHEN NULLIF(budget, 0) IS NULL OR NULLIF(budget, 0) IS NULL THEN 1
      ELSE 0
      END
    ) AS NUMERIC(10,2)) / 
    CAST(COUNT(1) AS NUMERIC(10,2))
    , 2)                AS perc_records_null
FROM movies_metadata


