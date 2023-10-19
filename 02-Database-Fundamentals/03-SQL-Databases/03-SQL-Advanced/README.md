## 🎯 Goal

Now we're switching to a field more relevant for "Data Analysts". Lets assume the data is clean, your data engineers have written a bunch of tests upstream in the pipeline, and they are all green 👍. You're being asked from a business stakeholder to answer a couple of questions about the film industry.

What we're trying to get out of this analysis is whether producers manage to produce movies that are more and more profitable over time.

Concepts:
- Subquery factoring with Common Table Expression (`WITH`)
- Window Functions (`OVER`)
- Mathematical operations on columns.

## Tasks

First, copy your `.env` file from the previous challenge to inside this challenge's folder. We'll need it again to be able to run the tests, which will connect to your database.

**❓ Write a query** that provides the absolute profit done by each movie, as well as its profit percentage (rounded to 2 decimals), for the movies that have both a `budget` and a `revenue` populated - meaning those 2 fields are not empty, and not equal to 0. Rank the movies by the most profitable movies in terms of profit percentage. Profit percentage is defined as `(Revenue - Budget) / Budget`.

Your output should at least contain 3 fields :
- the `id` of the movie
- a `profit_absolute`
- and a `profit_percentage`

The data still seems to not be that clean: there are records where the `budget` and the `revenue` are extremely low and don't seem to reflect the reality. **❓ Rewrite this query** focusing on movies that have both a `budget` and a `revenue` > 10,000.

🧪 Store your code in `exercice-1.sql` and `pytest tests/test_exercice_1.py` to check your results

<br>

**❓ What's the average absolute profit, the average revenue, and the average profit percentage per year?**
- Order your output by the most recent year, still excluding movies with a `budget` or a `revenue` <= 10,000.
- The output of the query should be 4 columns:
    - `release_year`
    - `avg_revenue` (Rounded to 0 decimal)
    - `avg_profit_absolute` (Rounded to 0 decimal)
    - `avg_profit_perc` (Rounded to 2 decimals)

🧪 Store your code in `exercice-2.sql` and check your results with `pytest tests/test_exercice_2.py`

<br>

As a follow up from the previous question, let's focus on profit as a function of time: **❓ What's the % of growth year over year for the `avg_profit_absolute`?**.
- Add this new columns to the previous output. You should have 5 columns:
    - `release_year`
    - `avg_revenue`
    - `avg_profit_absolute`
    - `avg_profit_absolute_perc_growth_yoy` (NEW one: Rounded to 0 decimal. e.g: 41 for 41% increase compared with previous year)
    - `avg_profit_perc`

<details>
  <summary markdown='span'>💡 Hints</summary>

Checkout `LEAD()` SQL function
</details>

🧪 Store your code in `exercice-3.sql` and `pytest tests/test_exercice_3.py`

<br>


Since question 1, we've been excluding movies where the `revenue` or the `budget` were not populated well because < $10,000. This challenges a lot the conclusions we could draw from our analysis. The underlying concept we're addressing here is called "Data Quality".

**❓Could you evaluate the % of bad data that populates this profit table**.

- E.g. What's the percentage of movies that have either a budget or a revenue not populated (NULL) or equal to 0? Watch out when doing your division (you can check online how to fix the fact that divisions of integers may return 0).
- Your output should have 3 columns :
    - `num_records_bad` (budget or revenue is NULL or equal to 0)
    - `num_records_total` (total number of records in the table)
    - `perc_records_bad` (percentage of records where budget or revenue is NULL or equal to 0). Rounded to 0 decimals
- Store your code in `exercice-4.sql`.

<br>

**🏁 Congratulations for making it here! 🧪 `make test` to check all your results at once, and _Push_ your code so we can track your progress!**

## Optional: Read and understand our tests
- Try to wrap your head around our `tests` folder in this challenge to see how they work
- In particular, notice how we use `lewagonde.read_sql_query` (option-click on a method in VS-code to Go-to-definition) and `psycopg2` to query your database with your own username & password, and convert query results to a pandas dataframe.
