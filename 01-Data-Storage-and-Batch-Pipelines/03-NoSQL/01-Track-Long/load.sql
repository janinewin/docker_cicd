TRUNCATE movies_metadata;
COPY movies_metadata
FROM '/files/movies_metadata_normalized.csv'
DELIMITER ','
CSV HEADER;

-- Delete the table contents with TRUNCATE
TRUNCATE tags_map;
COPY tags_map
FROM '/files/tags_map.csv'
DELIMITER ','
CSV HEADER;

-- Load the /files/tags.csv into the `tags` table
-- YOUR CODE HERE
