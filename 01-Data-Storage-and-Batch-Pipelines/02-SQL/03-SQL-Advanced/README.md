## Goal of this section

Now we're switching to a more "Data Analyst" type of question. Provided the data is clean (your data engineers have written a bunch of tests upstream in the pipeline, and they're all green), you're being asked from a business stakeholder to answer a couple of questions about the film industry. 

What we're tying to check out of this exercice is whether producers manage to produce movies that are more and more profitable over time. 

Concepts : 
- `JOIN`
- Operations on columns

## Exercices


1. --
  - (1.1) Write a query that provides the absolute profit done by each movie, as well as its profit percentage (rounded with 2 decimals), for the movies that have both a `budget` and a `revenue` populated. Rank the movies by the most profitable ones in terms of profit percentage [Working with basic column operations].
  - (1.2) The data still seems not very clean : there are records where the `budget` and the `revenue` are extremely low, and don't seem to reflect the reality. Rewrite this query, focusing on movies that have both a `budget` and a `revenue` > 100 000.
2. Each year, what's the average absolute profit and the average profit percentage ? Order your output by the most recent year, and filter out movies with a `budget` or a `revenue` <= 100 000. [Working with `GROUP BY` and aggregation operations]. The output of the query should be 3 columns :
  - `release_year`
  - `avg_profit_absolute` (Rounded to 0 decimal)
  - `avg_profit_perc` (Rounded to 2 decimals)
3. As a followup from question 3 : add a new column to the previous output : what's the % of growth year over year for both `avg_profit_absolute` and `avg_profit_perc` columns ? [Working with `WINDOW` functions]. The output of the query should be 4 columns :
  - `release_year`
  - `avg_profit_perc`
  - `avg_profit_perc_growth_yoy`
  - `avg_profit_absolute`
  - `avg_profit_absolute_growth_yoy`
4. Since question 1 : we've been excluding movies where the `revenue` or the `budget` were not populated well. This challenges a lot the conclusions we could draw from our analysis. The underlying concept we're addressing here is called "Data Quality". Could you evaluate the % of bad data that populates this table, when it comes to `profit` calculations ? E.g. What's the percentage of movies that have either a budget or a revenue not populated (NULL) or equal to 0 ? Watch out when doing your division (you can check online how to fix the fact that divisions of integers may return 0)
