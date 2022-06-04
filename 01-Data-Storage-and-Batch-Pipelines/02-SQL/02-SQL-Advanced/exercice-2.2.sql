SELECT 
    id
  , original_title
  , revenue 
  , budget
  , revenue - budget                        AS profit_absolute
  , ROUND((revenue - budget) / budget, 2)   AS profit_percentage
FROM movies_metadata
WHERE budget > 100000
AND revenue > 100000
ORDER BY ROUND((revenue - budget) / budget, 2) DESC
