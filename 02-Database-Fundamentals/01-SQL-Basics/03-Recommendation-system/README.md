# Recommendation System

The goal of this exercise will be to leverage the full text search capacity of postgres to build a recommendation system for films. We will be using the same database as before so bring across your `.env`

We will be using the same database as before so bring across your `.env`

```bash
cp ../01-Setup/.env .
```


## Tasks

### Task 1: Text Search with Ranking

#### Objective:

Find films in the Pagila database that are related to the word "Cat" based on their `description`. Also, rank the films by the relevance of the keywords in the `description`.

#### Instructions:

1. Use the `to_tsvector` function to convert the `description` column to a text-search vector.
2. Use the `@@` operator to perform the actual text search.
3. Utilize the `ts_rank` function to rank your results by relevance.
4. Sort your results by the rank in descending order.

Once you have a query put it in `text_search_query.sql` and run

```bash
make test
```

### Task 2: Simple Recommendation Engine

#### Objective:

Given a film title 'APOCALYPSE FLAMINGOS', recommend other films with similar `description`s.

#### Instructions:

1. Create a CTE (Common Table Expression) that holds the text-search vector of the `description` of the given film.
2. Use the CTE to find similar films based on the `description` text-search vector.
3. Ensure that the film used in the CTE is not included in your final list of recommendations.

Once you have a query put it in `recommendation_query.sql` and run

```bash
make test
```

### Task 3: Improved query ranking

#### Objective:

Improve the original query by using `ts_rank_cd` instead of `ts_rank` this time looking at 'Cat & Dog'

#### Instructions:

1. Use the `ts_rank_cd` function to rank your results by relevance.

Once you have a query put it in `improved_text_search_query.sql` and run

```bash
make test
```

### Task 4 (optional) Put it in a python script

Try to implement the recommendation.py script following the doc strings




## 🏁 Finished

We now have a cool way to recommend new movies! 🎉
