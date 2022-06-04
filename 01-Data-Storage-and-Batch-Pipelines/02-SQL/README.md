## Prerequisites

Make sure you have installed

- Poetry
- Docker

## Recap from yesterday and high level goals of the day

You've learnt the basics of building a Docker image, as well as setting up a base Docker Composer with FastAPI. Today we'll add 2 new components to the Docker Compose : postgres, and adminer
- Postgres is a database on which the data will be stored
- Adminer is a tool that provides a UI interface to write SQL queries on top of data you've imported.

The day is made of 4 steps:

1. Download a set of files that will be used in Day 2 and Day 3
2. Create the tables on PostGres where the data will be stored
3. "Migrate" the data from the csvs into the tables, using some simple mapping : some of the fields in the csv have a complex structure (JSONs), we'll simply treat this data as TEXT first, and will address them specifically in Day 3 and 4.
4. Deep diving into this dataset :
  - Understanding its structure, and the properties of the data in it
  - Getting some business insights about this data

## In which order should you address each section

- First, you should complete the `00-Setup-Exercice` section which makes you build the end to end pipeline of Day 2, but with a very simple file to load : `teacher.csv`
- Second, you should complete the `Track-long` section, which makes you load some of the key files of the Kaggle movies dataset in Kaggle into Postgres tables : [The Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset?resource=download
- Third, you should complete the `01-SQL-Basics`, `02-SQL-Advanced`, `03-SQL-More-Advanced` sections, which make you use SQL to answer business questions related to the movies dataset.
- If you have time, you can explore the `04-Data-Modeling-Optional` section, but it's not mandatory.
