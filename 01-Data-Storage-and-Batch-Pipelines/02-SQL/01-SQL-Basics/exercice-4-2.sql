
-- Test is failing as well

SELECT DISTINCT
-- DISTINCT is important here - since if movieId No 8 
-- is rated 1000 times in the ratings table. But the id 8 does not exist in 
-- the movies_metadata table : it prevents the query from outputing movieID = 8 1000 times.
    R.movie_id AS movie_id_ratings_table
  , MM.id     AS movie_id_movies_metadata_table
FROM ratings AS R 
  LEFT JOIN movies_metadata AS MM 
    ON R.movie_id = MM.id
-- Extracting records where the movie ID could not be found in the 
-- movies_metadata table
WHERE MM.id IS NULL 
