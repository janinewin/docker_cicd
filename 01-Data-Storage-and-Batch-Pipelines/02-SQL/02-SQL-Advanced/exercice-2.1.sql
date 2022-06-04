SELECT 
    id
  , original_title
  , revenue 
  , budget
  , revenue - budget                        AS profit_absolute
  , ROUND((revenue - budget) / budget, 2)   AS profit_percentage
FROM movies_metadata
WHERE NULLIF(budget, 0) IS NOT NULL
AND NULLIF(budget, 0) IS NOT NULL
ORDER BY ROUND((revenue - budget) / budget, 2) DESC
