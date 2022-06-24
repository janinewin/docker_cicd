# Week 2 - Day 2 - Track-long exercise

Yesterday we got familiar with the Hacker news dataset. We loaded it as a bulk. Today, instead of loading its entirety, we'll pretend the data is only available chunk by chunk (instead of all 14GB at once!). This will allow us to play with actual data, but in more real-time and realistic scenarios.

We will reuse the SQL queries and data pipelines from day 1. But this time, we'll implement them using serverless functions.

## Desired outcome

The students will:

On Google Cloud:

1. Create cloud functions that react to new Hacker News data made available
2. These functions will load the BigQuery database with the newer chunks of available data

Locally:

1. Use OpenFAAS
2. Store in Postgres
