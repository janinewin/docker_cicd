ALTER TABLE ratings ADD COLUMN created_at_utc TIMESTAMP;
INSERT INTO ratings (
  created_at_utc
)
SELECT 
  TO_TIMESTAMP(timestamp) AS created_at_utc
FROM ratings;
