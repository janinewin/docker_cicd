# Streamlit 📈

## Set-up

### End Goal 🏁
By the end of the setup, you should have a working stack using docker-compose (PostgreSQL, Streamlit) with the Formula 1 database loaded into PostgreSQL after running a SQL script in DBeaver. You will be able to access the Streamlit app at http://localhost:8501.

### Instructions 📔
1. Run `make download-sql-file`. This will download a SQL file that you need to run in DBeaver in order to create the data for today (we will do this in a later step).

2. In the `docker-compose-basic.yml` file - create the database service:
- based on PostgreSQL 14
- with a Restart policy: `Always`
- Loading the database f1db.sql located in `database/init/f1db.sql` into PostgreSQL leveraging volumes and the image's entrypoint `/docker-entrypoint-initdb.d/`
- with the Environment variables:
```yaml
- POSTGRES_DB=f1db
- POSTGRES_PASSWORD=postgres
- POSTGRES_USER=postgres
```

3. Create the Streamlit service
- Building the image located at the root folder
- with a Restart policy: `Always`
- Mounting the root folder into `/app/`
- Mounting the `./.streamlit` folder into `/app/.streamlit/`
- Opening the port 8501
- Depending on the database service


### Connecting Streamlit to the database 🔗
To connect a Streamlit app to the database, we need to create a secrets file to store our database credentials. This file, which is in the `.toml` format, is never committed to Git and should always be kept private and secure. Streamlit automatically loads and parses this file at runtime if it is in the correct location, similar to how an `.env` file is used.

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

3. Run `docker-compose -f docker-compose-basic.yml up`
4. You should be able to access the Streamlit app at http://localhost:8501
5. Run the sql script of `01-Streamlit/database/init/f1db.sql` to load the tables
into the Postgres database through the DBeaver interface (if this did not happen automatically). Use the values from the `secrets.toml` file to log into DBeaver.
6. Head to http://localhost:8501 👉 to see the dashboard✨

🚀 You are now ready to continue with the UI implementation.

## Data 📋
We are going to use real Formula 1 data. The goal of this exercise is to get you familiar with the basic functionality of Streamlit, while exploring the Formula 1 dataset.

## Streamlit basics 😎
Use the [documentation](https://docs.streamlit.io/library/api-reference) of Streamlit to help you.

In the `f1dashboard` folder there is a file called `basic.py`. It is already
partly filled with code, but your goal is to enhance the main Streamlit page
with the following:
- Add the right caching decorator to the `load_data()` function
- Create a Streamlit subheader using the `create_main_page()` function. You should also have a title and subheader in the sidebar.
- Do some summary statistics on the data using the `describe()` method from the `Pandas` package
- Create a bar chart that shows the number of points for the 5 best-performing drivers in descending order (show the driver with the most points on the left side of the graph). Write a query in the `top_driver()` function to retrieve the data and create a bar chart under `if __name__ == '__main__':` after having assigned the data to `top_driver_data`.
- Create a line chart with the number of points for the driver **Lewis Hamilton** over the years
- The data that is loaded needs to be stored into the session state for it
to be reusable across different pages in Streamlit, implement that functionality in the `session_state()` function.

**Commit and push** your code when you are finished.✨

## Streamlit advanced 😱
- Copy and paste the contents of `docker-compose-basic.yml` to `docker-compose-advanced.yml`, but change the Streamlit file that you run from `command: ["streamlit", "run", "f1dashboard/basic.py"]` to `command: ["streamlit", "run", "f1dashboard/advanced.py"]`.
- Run `docker-compose -f docker-compose-advanced.yml up`
- Convert your basic application into a multi-page app. In the `pages` folder there are two files. Each of these files create a separate page in the Streamlit app, which is visible in the sidebar. To keep the app clean, you can implement different parts of your application functionality on different pages. To also keep your code clean you are also going to separate the code that you created in `basic.py` into different files. All things considered, use the following structure:
  - `pages/01_descriptives.py` - Import the relevant libraries, load the data and implement your `summary_statistics` function here
  - `pages/02_visualizations.py` - Import the relevant libraries, load the data and move your visualizations to this page
  - `advanced/database.py` - For initializing the database connection
  - `advanced/cache.py` - The session_state() function
  - `advanced/constants.py` - The constants that you use in your code
  - `advanced/queries.py` - Your queries for retrieving the data
  - `advanced/transforms.py` - Any additional Python transformations if needed
  - `advanced.py` - The code with the Streamlit commands on the main page, this is the file where all the results come together and you use Streamlit commands to show the results on the web page.

## Storytelling 📢
Now that the engineering structure is in place, it is time to explore the data further 📊 . You have been assigned to a Formula 1 team in pairs, and it is your job to give a presentation to the management of your team (played by the TA and teacher) on how well you think your team will perform in 2019 based on data from previous years. 📈

In addition to discussing your team's performance, the CTO (also us) is interested in learning about the technical details of your Streamlit application. Therefore, you should create an extra page in your Streamlit app where you explain how you ensure that your web app stays fast, even if the amount of data increases.

Some analytical questions that you should answer in your presentation include:

- How many points has your team scored over the years?
- Who are your current drivers?
- If a driver is not performing well, which drivers from other teams should your team consider getting?
- What has historically been the best racetrack for your team? 👍
- What has been the worst racetrack? 👎
- Which two teams are your closest competitors? 💥

Use your creativity to come up with additional analysis if you have time. Support your analysis using Streamlit titles and text using Markdown. At the end of the day, we will ask you to present your findings to the group using your Streamlit application 📉. There is no need to create any slides for your presentation.
