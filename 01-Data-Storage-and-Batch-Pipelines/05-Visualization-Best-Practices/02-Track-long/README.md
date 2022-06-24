# Dashboard


For this exercise we will reuse the stack created on day 4. So far we have:

- set up a base Docker Compose with Postgres, FastAPI and Adminer. Today we'll load some data into this database.
- loaded a data schema mapping the [the movies dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset), and
- added a Jupyter lab environment to interact with the datasets and propose a new normalized SQL schema
- loaded periodically the latest comments using an Airflow DAG.


Today, we'll add a dashboard to visualize what we've done so far! The dashboard will have 2 panels:

1. Show the 5 movies with the best rating score (we can define a rating score as the rating's median for instance)
2. Given a movie (add a filter to the panel), show the 10 latest comments

## End goal
At the end of this exercise you should be able to:
- Add metabase in a docker compose stack
- Back up metabase data using a docker volume
- Connect a database to metabase and display all the data
- Create a dashboard with insighful cards

## Tasks

This exercise will walk you through all the steps to get a dashboard up and running in a docker compose stack

### 1. Setting up Metabase
1. Create a new metabase service, pulling the [metabase image](https://hub.docker.com/r/metabase/metabase/)
2. Adjust the restart policy to `always`
3. Let's back up the metabase internal DB based on [H2](https://www.h2database.com/html/main.html): Create a volume mapping the local dir `metabase-data` to the container dir `metabase-data`. This is where the internal DB will be located
4. Configure the location of Metabase's internal DB by ajusting the env var `MB_DB_FILE` with the current value: `/metabase-data/metabase.db`
5. Map port 3000 so you can access metabase on http://localhost:3000
6. Add a dependency for this service on the database service - the service spinning up the actual postgres database
7. Spin up the docker compose stack and wait for all the init to happen `docker-compose up`
8. Once ready, head to your http://localhost:3000
9. **Add your data later**
10. Get started with Metabase you should be able to explore the default dataset included with Metabase

### 2. Connecting the postgreSQL database to Metabase
1. Click on `add your own data`
2. Fill in all the information regarding your database
3. Wait until import is done
4. Exit admin interface
5. You should see all the tables on the home page

**NB: You can always explore the DB using adminer, the interface is ideal for prototyping SQL queries and understanding the schema**

### 3. Creating the metrics

**❓ #1: Let's show the 5 movies with the best rating score** (we can define a rating score as the rating's median for instance).
If you prefer you can either use the UI filters or just write a SQL query to get the answers.

**Let's start by computing the average rating for all the movies**

1. Click on New in the top right corner and select `Question`
2. Pick the database `movies`
3. Show the table ratings
4. Now compute the average rating for each movie
5. Save it then add it to a new dashboard
6. Save the dashboard
5. Once done you can explore the data and save the question to be reused later

**Let's compute the median rating**

1. Now create a new question and instead of `database` as starting point, choose a model and select the model just created
2. Now let's compute the median rating for all the ratings 
  - With SQL
  ```
  SELECT PERCENTILE_CONT(0.5)
  WITHIN GROUP (ORDER BY rating) AS median
  FROM ratings;
  ```
  - Without SQL you can explore the list of [available expression in metabase](https://www.metabase.com/docs/latest/users-guide/expressions-list.html#median) and use the UI filters.
3. Save the question and add it to your dashboard

**Finally let's get the top 5 movies with the best rating score**

1. Start with the `movies_metadata` table
2. Click on the join icon and join the ratings table on `movie_id`
3. Now compute the median using a custom expression
4. Aggregate by movie id
5. Order by median DESC
6. Limit to 5 rows 
  <details>
    <summary markdown='span'>Hint 💡</summary>
    You notice that nothing is showing up and that the median rating is `NULL`.
    Can you find out why, and correct the query?
  </details>
  <details>
    <summary markdown='span'>Help 🙌</summary>
    Exclude the movies where rating is empty/null.
  </details>

**Add it to your dashboard!**


**❓ #2: Given a movie (add a filter to the panel), show the 5 best comments and 5 worsts comments.**