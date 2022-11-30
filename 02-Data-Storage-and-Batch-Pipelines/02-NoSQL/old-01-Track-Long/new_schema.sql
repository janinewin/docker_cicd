-- Drop all tables
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS tags_map;
DROP TABLE IF EXISTS movies_metadata;

CREATE TABLE ratings (
    user_id     INT
  , movie_id    INT
  , rating      NUMERIC
  , timestamp   BIGINT
);

CREATE TABLE movies_metadata (
    adult                   BOOLEAN
  , budget                  FLOAT
  , homepage                TEXT
  , id                      INT
  , imdb_id                 VARCHAR(50)
  , original_language       VARCHAR(50)
  , original_title          TEXT
  , overview                TEXT
  , popularity              NUMERIC
  , poster_path             TEXT
  , release_date            DATE
  , revenue                 NUMERIC
  , runtime                 NUMERIC
  , status                  VARCHAR(50)
  , tagline                 TEXT 
  , title                   TEXT
  , video                   BOOLEAN
  , vote_average            NUMERIC
  , vote_count              INT
);

CREATE TABLE tags (
  name TEXT,
  value TEXT
);

-- Add the tags_map table
-- It has a movie_id INT column
-- It has a tag_value TEXT column
-- It has a tag_name TEXT column
-- YOUR CODE HERE
