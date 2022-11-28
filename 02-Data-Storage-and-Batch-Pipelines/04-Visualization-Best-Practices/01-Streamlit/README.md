# Streamlit
In this exercise we'll first setup a simple PostgreSQL, Adminer, [Streamlit](https://streamlit.io/) stack using docker compose. The new tool we are introducing, Streamlit is a convenient python solution to create simple UI to showcase data from various sources. It can be used to present data into custom dashboards, or simply used to create a python web app.

## End Goal
By the end of this exercise you should:
- Have a working stack using docker-compose (PostgreSQL, Adminer, Streamlit)
- Have The Formula 1 database loaded into PostgreSQL
- Be able to check out [http://localhost:8501](http://localhost:8501)

## Exercise
1. As usual, run the `make install` at the root directory of this exercise if you haven't done so. This will add all the necessary dependencies and download the necessary content for the day.

2. In the docker-compose file - Create the database service:
- based on PostgreSQL 14
- with a Restart policy: `Always`
- Loading the database f1db.sql located in `database/init/f1db.sql` into PostgreSQL leveraging volumes and the image's entrypoint `/docker-entrypoint-initdb.d/`
- with the Environment variables:
```yaml
- POSTGRES_DB=f1db
- POSTGRES_PASSWORD=postgres
- POSTGRES_USER=postgres
```

4. Create the adminer service
- Open the port 8080
- with a Restart policy: `Always`
- Depending on the database service

5. Create the Streamlit service
- Building the image located at the root folder
- with a Restart policy: `Always`
- Mounting the root folder into `/app/`
- Mounting the `./.streamlit` folder into `/app/.streamlit/`
- with command : `["streamlit", "run", "basic/main.py"]`
- Opening the port 8501
- Depending on the database service

6. Head to http://localhost:8501 👉 you should see the welcome service ✨
7. Run the sql script of `01-Streamlit/database/init/f1db.sql` to load the tables
into the Postgres database.

## Connecting to the database
Before we can build our Streamlit app, we need to add a secrets file for Streamlit to store our credentials in. We need this to connect to the database. Secrets files are never committed to git and should always be private or very well secured. The secret file for Streamlit is a simple `.toml` file that Streamlit automatically loads and parses at run time if in the correct location. Simply put, it is equivalent to an `.env` file.

1. In the `.streamlit` folder there is an existing config file responsible for the configuration of a few key elements in Streamlit. In the same folder add a `secrets.toml` file

2. In the `secrets.toml` file add the required credentials to connect to the PostgresSQL instance
    ```toml
    [postgres]

    drivername = "postgresql"
    host = "database"
    port = 5432
    database = "f1db"
    username = "postgres"
    password = "postgres"
    ```
You are now ready to continue with the UI implementation.

## Data
We are going to use real Formula 1 data. The goal of this exercise is to get you familiar with the basic functionality of Streamlit, while exploring the Formula 1 dataset.

## Streamlit basics
In the `app` folder there is a file called `main.py`. It is already
partly filled with code, but your goal is to enhance the main Streamlit page
with the following:
- Add the right caching decorator to the `load_data` function
- Create a Streamlit title, subheader on the main page. Do the same in the sidebar
- Do some summary statistics on the data using the `describe()` method from the `Pandas` package.
- Create a bar chart that shows the number of points for the 5 best-performing drivers in descending order (show the driver with the most points on the left side)
- Create a line chart with the number of points for the driver **Lewis Hamilton**
- The data that is loaded needs to be saved into the session state for it
to be reusable across different pages in Streamlit, implement that functionality

Use the [documentation](https://docs.streamlit.io/library/api-reference) of Streamlit to help you.

Commit and push your code when you are finished.

## Streamlit advanced
- Create a multi-page app. See the Streamlit documentation
for more info on how this works. Create one file for doing descriptive
statistics, and another one for visualizing the data. Also separate your other code into different files. Use the following structure:
  - `main.py` - The code with your Streamlit commands on the main page
  - `pages/descriptives.py` - Descriptive statistics of your data sources
  - `pages/visualizations.py` - Your data visualizations on a separate page
  - `f1_cache.py` - your code for caching
  - `f1_constants.py` - the constants that you use in your project
  - `f1_database.py` - for initializing the database connection
  - `f1_queries.py` - write your queries for retrieving the data
  - `f1_transforms.py` - any additional Python data transformations if needed


## Storytelling
Now that the engineering structure is in place, it is time to further explore the data.
