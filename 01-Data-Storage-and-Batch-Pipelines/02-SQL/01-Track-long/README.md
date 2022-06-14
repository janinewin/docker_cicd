## High Level Description 

You'll reproduce the steps done in `00-Setup` but with some more complex files. The goal is to have a database structure ready to then execute SQL queries on it in the `02-SQL-Basics`, `03-SQL-Advanced` sections

## Steps

- Go to the movies dataset in Kaggle : [The Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset?resource=download), and download the 7 files into the `02-SQL/00-Setup-Exercise/data/files` folder : 
  - `credits.csv`
  - `keywords.csv`
  - `links_small.csv`
  - `links.csv`
  - `movies_metadata.csv`
  - `ratings_small.csv`
  - `ratings.csv`
- We'll load the data from `movies_metadata.csv`, and `ratings.csv` in Postgres.
- Relaunch your `docker-compose` to port those files to your postgres container

### `movies_metadata.csv`
1. Create a `movies_metadata` table using SQL commands in Adminer, which contains the exact same columns as the ones in the `movies_metadata.csv` file. For the column types, let's be flexible and use only 5 different types : 
  1.1 `VARCHAR(50)` - when you feel like the length of the data in this field should be limited
  1.2 `TEXT` - when you feel like the length of the data in this field could be big
  1.3 `INT` - if all records in this field seem to be integers
  1.4 `NUMERIC` - if the records may contain decimals
  1.5 `DATE` - self explanatory
(To explore the structure of the file, you can use bash commands to extract only the first 3 rows)
_Note : Running the same "table creation" SQL script again, after the table is already created should not fail_
2. Load the data from this `csv` into the `movies_metadata` table. 3 records are corrupted in the CSV file. Can you identify why ? Fix those records manually. 
Hint : those are the breaking rows:
  2.1 Line 19763 (ID = 82663)
  2.2 Line 29571 (ID = 122662)
  2.3 Line 35669 (ID = 249260)
3. We were flexible in the way we were loading data : strings were loaded either as a `VARCHAR(50)` or as `TEXT`. In reality, `adult` and `movies` should be `BOOLEAN` : change the data type of those 2 columns to `BOOLEAN`

### `ratings.csv`
Follow the same steps as for the `movies_metadata.csv` file
1. Create the corresponding table. The columns should be named differently than in the csv (camelCase is not a standard way of naming fields in tables. snake_case is preferred)
  1.1 user_id
  1.2 movie_id
  1.3 rating
  1.4 timestamp
2. Load the data from the csv in the destination table (it should take a while : the file is almost 1GB large and contains more than 26 million rows)
3. The `timestamp` column is in a format called "epoch". Check what it means online, and, in a column called `created_at_utc`, load its equivalent in more readable `YYYY-MM-DD HH:MI:SS` format. (The query should take ~5-6 minutes to run)
