COPY movies_metadata
FROM '/files/movies_metadata.csv'
DELIMITER ','
CSV HEADER;


