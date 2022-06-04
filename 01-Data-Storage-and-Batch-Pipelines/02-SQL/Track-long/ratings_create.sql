DROP TABLE IF EXISTS ratings;
CREATE TABLE ratings (
    user_id     INT
  , movie_id    INT
  , rating      NUMERIC
  , timestamp   BIGINT
);
