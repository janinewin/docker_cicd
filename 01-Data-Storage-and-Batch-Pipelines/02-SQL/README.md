## Prerequisites

Make sure you have installed

- Poetry
- Docker

## Recap from yesterday and high level goals of the day

You've learnt the basics of building a Docker image, as well as setting up a base Docker Composer. Today we'll focus only on 2 new components of the Docker Compose : postgres, and adminer.
- Postgres is a database on which the data will be stored
- Adminer is a tool that provides a UI interface to write SQL queries on top of data you've imported.

The day is made of 4 steps:

1. Download a set of files that will be used in Day 2 and Day 3
2. Create the tables on PostGres where the data will be stored
3. "Migrate" the data from the csvs into the tables, using some simple mapping : some of the fields in the csv have a complex structure (JSONs), we'll simply treat this data as TEXT first, and will address them specifically in Day 3 and 4.
4. Deep dive into this dataset :
  4.1. Understand its structure, and the properties of the data in it
  4.2. Get some business insights about this data

## In which order should you address each section

- First, you should complete the `00-Setup` section which makes you build the end to end pipeline of Day 2, but with a very simple file to load : `teacher.csv`
- Second, you should complete the `01-Track-long` section, which makes you load some of the key files of the Kaggle movies dataset in Kaggle into Postgres tables : [The Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset?resource=download
- Third, you should complete the `02-SQL-Basics`, `03-SQL-Advanced`, which make you use SQL to answer business questions related to the movies dataset.
- If you have time, you can explore the `04-Recap` section, which we will address during the Live Code at the end of the day.
