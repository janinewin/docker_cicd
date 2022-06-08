SELECT
    column_name
  , data_type
  , is_nullable
  , ordinal_position
FROM INFORMATION_SCHEMA.COLUMNS
WHERE table_name = 'movies_metadata'
ORDER BY ordinal_position
