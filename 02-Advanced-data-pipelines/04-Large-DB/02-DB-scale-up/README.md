# Scaling a database

Database access patterns determine what to optimize for. A database gives us mainly three tools to make queries more efficient:

- adding indexes
- (materialized) views
- a schema redesign

In this exercise, we'll explore all three as well as their pros and cons. We'll use our beloved Postgres database.

We'll load the [Ikea dataset](https://www.kaggle.com/datasets/crawlfeeds/ikea-us-products-dataset).

## Data transformation with Pandas

- Run a quick transformation using Pandas to load the data from a CSV

## Indexing

- Explore the types of indexes
- B-Tree indexes, add one, evaluate insert and read performance
- CSV loading and adding / removing an index

## Full-text search

- Load the dataset and search by keyword.
- Add full text search and querying in Postgres.

## JSON indexing

- Query a particular field.
- Index a particular field.

## Materialized view

- Add a materialized view on a complex dataset.
- Run a complex query, transform into a materialized view and compare.
