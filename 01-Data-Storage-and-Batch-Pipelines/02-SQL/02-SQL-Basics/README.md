## Goal

We need to explore the dataset available. This should be done in 3 steps
  - Understand the structure of the tables and the data types of the fields in those tables
  - Understand the concept of primary key, foreign key, and field constraints
  - Explore the data contained in the tables, make sure it's coherent and respects the constraints associated to their definitions (introducing the concept of SQL tests implemented on a data pipeline)

## Tasks

1. **❓ Write a query** that provides the list of tables in the database.
2. **❓ Write a query** that returns the list of columns and their data types in the `movies_metadata` table.
3. The `adult` column is a boolean column. Meaning its values should only be TRUE, or FALSE. 
**❓ Write a query** making sure that this column is never equal to any other value. 
<details>
<summary markdown='span'>💡 Hint</summary>
The way to write a test in SQL is to write a query that returns rows if the test fails. And returns no row if the test succeeds
</details>

4. **❓ Write 2 other tests**, and determines whether it succeeds, or fails.
  - One that checks the unicity of the `id` column. It fails if 2 records in this table share the same `id`. If it's indeed unique, then ID can be called a primary key.
    - If it fails, can you try to explain what cause some records to be duplicated?
  - One that checks for referential integrity: the `movie_id` column in the `ratings` table refers to the `id` column in the `movies` table. There would be a problem if a `movie_id` in the `ratings` table did not exist in the `movies` table. Check that this never happens.
