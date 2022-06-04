SELECT *
FROM movies_metadata
WHERE adult IS NOT TRUE 
AND adult IS NOT FALSE

/* Other possible solutions

SELECT *
FROM movies_metadata
WHERE adult NOT IN (TRUE, FALSE)

SELECT *
FROM movies_metadata
WHERE adult != TRUE 
AND adult != FALSE

*/
