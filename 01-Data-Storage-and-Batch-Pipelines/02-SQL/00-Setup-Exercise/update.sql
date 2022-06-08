-- Solution 1 (most compact)

ALTER TABLE movies_metadata ALTER COLUMN adult TYPE BOOLEAN USING 
  CASE
    WHEN adult = 'True' THEN TRUE
    WHEN adult = 'False' THEN FALSE 
  END;

ALTER TABLE movies_metadata ALTER COLUMN movie TYPE BOOLEAN USING 
  CASE
    WHEN movie = 'True' THEN TRUE
    WHEN movie = 'False' THEN FALSE 
  END;

-- Solution 2 (more verbose)
-- 2.1. Updating the content of the fields
-- 2.2. Converting those fields to BOOLEANs

UPDATE movies_metadata
SET 
    adult =
      CASE
        WHEN adult = 'True' THEN TRUE
        WHEN adult = 'False' THEN FALSE 
      END
  , video = 
      CASE
        WHEN video = 'True' THEN TRUE
        WHEN video = 'False' THEN FALSE 
      END;


ALTER TABLE movies_metadata ALTER COLUMN adult TYPE BOOLEAN USING adult::BOOLEAN;
ALTER TABLE movies_metadata ALTER COLUMN video TYPE BOOLEAN USING video::BOOLEAN;



