## Goal

We need to explore the dataset available. This should be done in 3 steps
  - Understand the structure of the tables and the data types of the fields in those tables
  - Understand the concept of primary key, foreign key, and field constraints
  - Explore the data contained in the tables, make sure it's coherent and respects the constraints associated to their definitions (introducing the concept of SQL tests implemented on a data pipeline)

## Tasks

1. **❓ Write a query** that provides the list of tables in the database. Store your code in `exercice-1.sql`.
2. **❓ Write a query** that returns the list of columns and their data types in the `movies_metadata` table. Store your code in `exercice-2.sql`.
3. The `adult` column is a boolean column. Meaning its values should only be TRUE, or FALSE. **❓ Write a query** that makes sure that this column is never equal to any other value. Store your code in `exercice-3.sql`.
    <details>
    <summary markdown='span'>💡 Hint</summary>
    The way to write a test in SQL is to write a query that returns rows if the test fails. And returns no row if the test succeeds
    </details>

4. **❓ Write 2 other tests**, and determines whether it succeeds, or fails.
    - [4-1-1] One that checks the unicity of the `id` column in the `movies_metadata` table. It fails if 2 records in this table share the same `id`. If it's indeed unique, then ID can be called a primary key. The output of your query should be a table with 2 columns : `id`, `num_records` (where `num_records` is the number of occurences observed for a given `id`). Example : if `id = 123` appears 17 times in the `movies_metadata` table, `num_records = 17` for `id = 123`. Store your code in `exercice-4-1-1.sql`.
      - [4-1-2] If it fails, can you try to explain what cause some records to be duplicated ? Store your code in `exercice-4-1-2.sql`
    - [4-2] One that checks for referential integrity: the `movie_id` column in the `ratings` table refers to the `id` column in the `movies` table. There would be a problem if a `movie_id` in the `ratings` table did not exist in the `movies` table. Check whether this happens or not. The output of the query should be 1 column, called `movie_id_ratings_table`, which lists all the **distinct** `movie_id` that exist in the `ratings` table but don't exist in the `movies_metadata` table. This query should take a long time to execute - and it will also increase the duration of your tests execution : so make sure you do this exercice at the very end. Store your code in `exercice-4-2.sql`
