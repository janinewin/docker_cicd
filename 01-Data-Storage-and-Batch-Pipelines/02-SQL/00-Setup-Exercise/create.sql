DROP TABLE IF EXISTS movies_metadata;
CREATE TABLE movies_metadata (
    adult                   VARCHAR(50)
  , belongs_to_collection   TEXT
  , budget                  INT
  , genres                  TEXT 
  , homepage                TEXT
  , id                      INT
  , imdb_id                 VARCHAR(50)
  , original_language       VARCHAR(50)
  , original_title          TEXT
  , overview                TEXT
  , popularity              NUMERIC
  , poster_path             TEXT
  , production_companies    TEXT
  , production_countries    TEXT
  , release_date            DATE
  , revenue                 NUMERIC
  , runtime                 NUMERIC
  , spoken_languages        TEXT
  , status                  VARCHAR(50)
  , tagline                 TEXT 
  , title                   TEXT
  , video                   VARCHAR(50)
  , vote_average            NUMERIC
  , vote_count              INT
);
