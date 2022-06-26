## Goal

Now we're switching to a more "Data Analyst" type of question. Provided the data is clean (your data engineers have written a bunch of tests upstream in the pipeline, and they're all green), you're being asked from a business stakeholder to answer a couple of questions about the film industry. 

What we're trying to get out of this analysis is whether producers manage to produce movies that are more and more profitable over time. 

Concepts: 
- `JOIN`
- Operations on columns

## Tasks


1. **❓ Write a query** that provides the gross profit done by each movie, as well as its profit percentage (rounded with 2 decimals), for the movies that have both a `budget` and a `revenue` populated - meaning those 2 fields are not empty, and not equal to 0. Rank the movies by the most profitable ones in terms of profit percentage. The profit percentage is defined as `(Revenue - Cost) / Cost`. Your output should at least contain 3 fields : the `id` of the movie, a `profit_absolute`, and a `profit_percentage`. Store your code in `exercice-1-1.sql`
  - The data still seems not very clean: there are records where the `budget` and the `revenue` are extremely low, and don't seem to reflect the reality. **❓ Rewrite this query**, focusing on movies that have both a `budget` and a `revenue` > 100 000. Store your code in `exercice-1-2.sql`
2. **❓ What's the average absolute profit, the average revenue, and the average profit percentage per year?** Order your output by the most recent year, and filter out movies with a `budget` or a `revenue` <= 100 000. Store your code in `exercice-2.sql`. The output of the query should be 3 columns:
  - `release_year`
  - `avg_revenue` (Rounded to 0 decimal)
  - `avg_profit_absolute` (Rounded to 0 decimal)
  - `avg_profit_perc` (Rounded to 2 decimals)
3. As a followup from the previous question, let's add new columns to the previous output: **❓ What's the % of growth year over year for `avg_profit_absolute` and `avg_profit_perc` columns?**. Store your code in `exercice-3.sql`. The output of the query should be 5 columns:
  - `release_year`
  - `avg_profit_perc`
  - `avg_profit_perc_growth_yoy`
  - `avg_profit_absolute`
  - `avg_profit_absolute_growth_yoy`
4. Since question 1, we've been excluding movies where the `revenue` or the `budget` were not populated well. This challenges a lot the conclusions we could draw from our analysis. The underlying concept we're addressing here is called "Data Quality". 
  - **❓Could you evaluate the % of bad data that populates this table, when it comes to `profit` calculations?**. E.g. What's the percentage of movies that have either a budget or a revenue not populated (NULL) or equal to 0? Watch out when doing your division (you can check online how to fix the fact that divisions of integers may return 0). Store your code in `exercice-4.sql`. Your output should have 3 columns : 
    - `num_records_bad` (budget or revenue is NULL or equal to 0)
    - `num_records_total` (total number of records in the table)
    - `perc_records_bad` (percentage of records where budget or revenue is NULL or equal to 0). Rounded to 2 decimals
