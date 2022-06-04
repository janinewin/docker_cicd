ALTER TABLE ratings ADD COLUMN IF NOT EXISTS created_at_utc TIMESTAMP;
INSERT INTO ratings (
  created_at_utc
)
SELECT 
  TO_TIMESTAMP(timestamp)
FROM ratings;
