-- Results do not match

WITH rating_avg_rebuilt AS (
  SELECT 
      movie_id              AS movie_id 
    , ROUND(AVG(rating), 2) AS avg_rating_rebuilt
  FROM ratings
  GROUP BY movie_id
)

SELECT 
    MM.id 
  , MM.original_title
  , ROUND(vote_average, 2) AS vote_average_rounded
  , avg_rating_rebuilt
FROM movies_metadata AS MM 
  LEFT JOIN rating_avg_rebuilt RA 
    ON MM.id = RA.movie_id 
WHERE ROUND(vote_average, 2) != avg_rating_rebuilt
