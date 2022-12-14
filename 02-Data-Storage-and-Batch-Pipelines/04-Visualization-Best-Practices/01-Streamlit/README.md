# Streamlit 📈

## Set-up
In this exercise, we will be setting up a simple PostgreSQL, Adminer, and Streamlit stack using docker-compose. Streamlit is a convenient Python solution for creating a simple UI to showcase data from various sources. It can be used to present data into custom dashboards or to create a Python web app.

### End Goal 🏁
By the end of the setup, you should have a working stack using docker-compose (PostgreSQL, Adminer, Streamlit) with the Formula 1 database loaded into PostgreSQL. You will be able to access it at http://localhost:8501.

### Instructions 📔
1. As usual, run the `make install` at the root directory of this day if you haven't done so. This will download the necessary content for the day.

2. In the `docker-compose-basic` file - Create the database service:
- based on PostgreSQL 14
- with a Restart policy: `Always`
- Loading the database f1db.sql located in `database/init/f1db.sql` into PostgreSQL leveraging volumes and the image's entrypoint `/docker-entrypoint-initdb.d/`
- with the Environment variables:
```yaml
- POSTGRES_DB=f1db
- POSTGRES_PASSWORD=postgres
- POSTGRES_USER=postgres
```

4. Create the Adminer service
- Open the port 8080
- with a Restart policy: `Always`
- Depending on the database service

5. Create the Streamlit service
- Building the image located at the root folder
- with a Restart policy: `Always`
- Mounting the root folder into `/app/`
- Mounting the `./.streamlit` folder into `/app/.streamlit/`
- Opening the port 8501
- Depending on the database service


### Connecting Streamlit to the database 🔗
To create a Streamlit app, we need to create a secrets file to store our database credentials. This file, which is in the .toml format, is never committed to Git and should always be kept private and secure. Streamlit automatically loads and parses this file at runtime if it is in the correct location, similar to how an .env file is used. This secret file is necessary for Streamlit to connect to the database.

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
4. Run the sql script of `01-Streamlit/database/init/f1db.sql` to load the tables
into the Postgres database through the Adminer interface. Use the values from the `secrets.toml` file to log into Adminer.
5. Head to http://localhost:8501 👉 to see the dashboard✨

🚀 You are now ready to continue with the UI implementation.

## Data 📋
We are going to use real Formula 1 data. The goal of this exercise is to get you familiar with the basic functionality of Streamlit, while exploring the Formula 1 dataset.

## Streamlit basics 😎
Use the [documentation](https://docs.streamlit.io/library/api-reference) of Streamlit to help you.

In the `app` folder there is a file called `basic.py`. It is already
partly filled with code, but your goal is to enhance the main Streamlit page
with the following:
- Add the right caching decorator to the `load_data` function
- Create a Streamlit title and subheader on the main page. Do the same in the sidebar
- Do some summary statistics on the data using the `describe()` method from the `Pandas` package
- Create a bar chart that shows the number of points for the 5 best-performing drivers in descending order (show the driver with the most points on the left side of the graph)
- Create a line chart with the number of points for the driver **Lewis Hamilton** over the years
- The data that is loaded needs to be stored into the session state for it
to be reusable across different pages in Streamlit, implement that functionality

**Commit and push** your code when you are finished.✨

## Streamlit advanced 😱
- Copy and paste the contents of `docker-compose-basic.yml` to `docker-compose-advanced.yml`, but change the Streamlit file that you run from `command: ["streamlit", "run", "app/basic.py"]` to `command: ["streamlit", "run", "app/advanced.py"]`.
- Convert your basic application into a multi-page app. See the Streamlit documentation
for more info on how this works. Create one file for descriptive
statistics, and another one for visualizing the data. Also separate the code that you created in `basic.py` into different files. Use the following structure:
  - `pages/01_descriptives.py` - Descriptive statistics of your data sources
  - `pages/02_visualizations.py` - Your data visualizations on a separate page
  - `advanced/cache.py` - your code for caching the data
  - `advanced/constants.py` - the constants that you use in your code
  - `advanced/database.py` - for initializing the database connection
  - `advanced/queries.py` - your queries for retrieving the data
  - `advanced/transforms.py` - any additional Python data transformations if needed
  - `advanced.py` - The code with the Streamlit commands on the main page, this is the file where all the results come together and you use Streamlit commands to show the results on the web page.

It is best-practice to separate your code into different files/classes/functions to keep it clean!


## Storytelling 📢
Now that the engineering structure is in place, it is time to explore the data further 📊 . You have been assigned to a Formula 1 team in pairs, and it is your job to give a presentation to the management of your team (played by the TA and teacher) on how well you think your team will perform in 2019 based on data from previous years. 📈

In addition to discussing your team's performance, the CTO (also us) is interested in learning about the technical details of your Streamlit application. Therefore, you should create an extra page in your Streamlit app where you explain how you ensure that your web app stays fast, even if the amount of data increases.

Some analytical questions that you should answer in your presentation include:

- How many points has your team scored over the years?
- Who are your current drivers?
- If a driver is not performing well, which drivers from other teams should your team consider getting? 👺
- What has historically been the best racetrack for your team? 👍
- What has been the worst racetrack? 👎
- Which two teams are your closest competitors? 💥

Use your creativity to come up with additional analysis if you have time. Support your analysis using Streamlit titles and text using Markdown. At the end of the day, we will ask you to present your findings to the group using your Streamlit application 📉 . There is no need to create any slides for your presentation.
