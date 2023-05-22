## Prerequisites

Make sure you've
- Enabled the BigQuery API and can run `gcloud` commands in your terminal

## Recap from last week and high level of the day

Last week, you've learnt how to setup a Database, pull data into a database, query from it, and visualise it. However

- you haven't dealt with large amounts of data
- you were not transforming the data much - your queries were used to display results and graphs, but were not stored physically, nor saved anywhere.

Today, you'll work exactly on that. Which concretelly means :
- you will build multiple layers of data quality :
  - a raw layer : the raw / un transformed data. The source data, essentially
  - a staging layer : an intermediate layer, where you've done a first pass of transformations on your data
    - converting types
    - renaming columns
    - converting timestamps etc
  - a mart layer : a layer where you build new interesting tables, that could be used by business stakeholders, and where you calculate new fields & metrics that initially didn't exist in the raw data
- you will setup DBT, which is the tool that enables you to structure a project around data transformations.
  - which knows when to write into which BigQuery project mentioned above
  - stores all your SQL queries + parameters needed to build your new tables / views

In the recap, you'll learn about how to setup a DEV and a PROD environment in BigQuery, using DBT.
- The DEV environement is where you can play around with data, build intermediate tables etc, using this environment as a sandbox
- The PROD environment is only accessible by 1 service account, which execute the code (table creation + data insertion) which has been reviewed and validated by peers.

## Planning of the day

So you should do the exercises in the correct order
- Setup BigQuery
- Setup DBT
- Build models in DBT in order to facilitate the analysis about the HackerNews data for your business stakeholders
