COPY ratings
FROM '/files/ratings.csv'
DELIMITER ','
CSV HEADER;

COPY movies_metadata
FROM '/files/movies_metadata.csv'
DELIMITER ','
CSV HEADER;

COPY tags_map
FROM '/files/tags_map.csv'
DELIMITER ','
CSV HEADER;

-- Load the /files/tags.csv into the `tags` table
-- YOUR CODE HERE
