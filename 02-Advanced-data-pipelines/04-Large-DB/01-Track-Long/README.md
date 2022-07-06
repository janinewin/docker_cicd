# Week 2 - Day 4 - Track-long exercise

Building on the setup from day 3, we'll switch databases to augment the load and move from Postgres to TimescaleDB.

In a second part of the exercise we'll add a queue, and instead of loading data into Timescale each time we receive it, we'll accumulate it and play with window size.

**TBD based on previous days**

## Desired outcome

The students will
- modify the stack to use TimescaleDB instead of Postgres
- add a queue to the system
- modify the Airflow DAG to push to the queue
- load data periodically from the queue
- measure performance metrics
