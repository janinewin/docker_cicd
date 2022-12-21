## 1️⃣ Set-up
<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D5/streamlit-logo.png" alt="drawing" width="200"/>

### 🎯 Goal
By the end of the setup, you should have a working stack using docker-compose (PostgreSQL, Streamlit) with the Formula 1 database loaded into PostgreSQL after running a SQL script in DBeaver. You will be able to access the Streamlit app at http://localhost:8501.

### Instructions
1️⃣ ❓ Run the following command to download a `SQL` file and place it in your `database/init/` subdirectory:
```bash
curl --output ./database/init/f1db.sql.gz https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/datasets/f1/f1db.sql.gz
```

2️⃣ ❓ You need to run the contents of this SQL file in DBeaver in order to create the data for today (we will do this in a later step). It is still zipped, unzip it yourself using the `gzip` command from the terminal.

3️⃣ ❓ In the `docker-compose-basic.yml` file - create the database service:
- based on PostgreSQL 14
- with a Restart policy: `Always`
- Loading the database f1db.sql located in `database/init/f1db.sql` into PostgreSQL leveraging volumes and the image's entrypoint `/docker-entrypoint-initdb.d/`
- with the Environment variables:
  - POSTGRES_DB=f1db
  - POSTGRES_PASSWORD=postgres
  - POSTGRES_USER=postgres
```

4️⃣ ❓ Create the Streamlit service
- Building the image (Dockerfile) located at the root folder
- with a Restart policy: `Always`
- Mounting the root folder into `/app/`
- Mounting the `./.streamlit` folder into `/app/.streamlit/`
- Opening the port 8501
- Depending on the database service


### Connecting Streamlit to the database 🔗
💡 To connect a Streamlit app to the database, we need to create a secrets file to store our database credentials. This file, which is in the `.toml` format, is never committed to Git and should always be kept private and secure. Streamlit automatically loads and parses this file at runtime if it is in the correct location, similar to how an `.env` file is used.

1️⃣ ❓ In the `.streamlit` folder there is an existing config file responsible for the configuration of a few key elements in Streamlit. In the same folder add a `secrets.toml` file

2️⃣ ❓ In the `secrets.toml` file add the required credentials to connect to the PostgresSQL instance
  ```toml
  [postgres]

  drivername = "postgresql"
  host = "database"
  port = 5432
  database = "f1db"
  username = "postgres"
  password = "postgres"
  ```

3️⃣ ❓ Run
```bash
docker-compose -f docker-compose-basic.yml up
```
☝️ You should be able to access the Streamlit app at http://localhost:8501.

4️⃣ ❓Run the sql script of `01-Streamlit/database/init/f1db.sql` to load the tables
into the Postgres database through the DBeaver interface (if this did not happen automatically). Use the values from the `secrets.toml` file to log into DBeaver. Head to http://localhost:8501 👉 to see the dashboard✨

🚀 You are now ready to continue with the UI implementation.

---

## 2️⃣ Streamlit basics 😎
🎯 We are going to use real Formula 1 data. The goal of this exercise is to get you familiar with the basic functionalities of Streamlit, while exploring the Formula 1 dataset 🚗.

📚 Use the [documentation](https://docs.streamlit.io/library/api-reference) of Streamlit to help you.

In the `f1dashboard` folder there is a file called `basic.py`. It is already partly filled with code, but your goal is to enhance the main Streamlit page with the following:

1️⃣ ❓ Add the right caching decorator to the `load_data()` function. The `load_data` function loads the data from the database.
<details>
  <summary markdown='span'>🤯 Why?</summary>

🤯  The caching mechanism makes sure that the loaded data is stored in the `cache` of Streamlit. The next time that the Streamlit script is run, the data does not have to be retrieved from the database, but can be retrieved from `cache`, speeding up the application.
</details>

2️⃣ ❓ We want to add some more written content to the web app! Create a Streamlit subheader in the `create_main_page()` function. Also create a title and subheader in the sidebar.

3️⃣ 💡 At the moment the `create_main_page()` function returns `races` as a string value. This value is used as input by the `load_data()` function to load the data. However, `races` is not the only table in the database. All table names are stored a list called `tables` (see the top of the `basic.py` file). ❓ Your job is to create a **[Streamlit selectbox widget](https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)** that uses this list as its input, and allows the user to select one of the tables. Return the selected table from the `create_main_function`.

4️⃣ ❓ Lets explore the data and do some summary statistics on the data using the `describe()` method from the `Pandas` package in the `summary_statistics` function.

5️⃣ ❓ Create a bar chart that shows the number of points for the 5 best-performing drivers in descending order (show the driver with the most points on the left side of the graph). Write a query in the `top_driver()` function to retrieve the data and create a bar chart under `if __name__ == '__main__':` after having assigned the data to `top_driver_data`. Use the `drivers` and `driver_standings` tables.

6️⃣ ❓ Create a line chart with the number of points for the driver **Lewis Hamilton** over the years, with years on the x-axis and the number of points on the y-axis. You need the `drivers`, `driver_standings` and `races` table.

7️⃣ ❓ The data that is loaded needs to be stored into the [session state](https://docs.streamlit.io/library/api-reference/session-state) for it to be reusable across different pages in Streamlit. Add the loaded_data into the Streamlit session state in the `session_state()` function. Validate that you can access the data on the `descriptives` page from the session state. See the [docs](https://docs.streamlit.io/library/api-reference/session-state) for more info.

💾  **Commit and push** your code when you are finished.✨

---

## 3️⃣ Engineering 😱
We have a basic Streamlit app now, which we have coded in a single python file. In order to make the app scalable and future-proof, we have some refactoring to do.

1️⃣ ❓ Copy and paste the contents of `docker-compose-basic.yml` to `docker-compose-advanced.yml`, but change the Streamlit file that you run from `command: ["streamlit", "run", "f1dashboard/basic.py"]` to `command: ["streamlit", "run", "f1dashboard/advanced.py"]`. Run `docker-compose -f docker-compose-advanced.yml up`

2️⃣ ❓ Convert your basic application into a [multi-page app](https://blog.streamlit.io/introducing-multipage-apps/). In the `pages` folder there are two files. Each of these files create a separate page in the Streamlit app, which is visible in the sidebar. To keep the app clean, you can implement different parts of your application functionality on different pages. All things considered, use the following structure:
  - `pages/01_descriptives.py` - Implement your `summary_statistics` function here. Implement the `selectbox` widget that you created before and assign it to `self.selected_table`, replacing the hard-coded `races` value with it. There is a list with the different tables in the `constants.py` file. You should be able to select one of these tables and get the descriptive statistics of that table.
  - `pages/02_visualizations.py` - Move your visualizations to this page. You can see that the data for the top drivers and for the points of Lewis Hamilton over the years is retrieved using the `get_data` function of the F1Cache class.
    <details>
      <summary markdown='span'>🤯 get_data?</summary>
    💡 How it works is that `get_data("top_drivers")` triggers the function of `top_drivers` in the `queries.py` file. Similarly, `get_data("lewis_over_the_years")` triggers the `lewis_over_the_years` function in `queries.py`. If you want to create a new function using this structure:
    1) Create the function in `queries.py` (e.g. called `get_fastest_lap_time`)
    2) Trigger it in the `02_visualizations` page using `get_data("get_fastest_lap_time")`. You are welcome to ignore this structure and write your own logic of course for retrieving data, this is only intended to help you out a bit.
    </details>

  - `advanced/queries.py` - Move your queries to retrieve the data here
  - `advanced.py` - The code with the Streamlit commands on the main page. You can move your titles and subheaders here.

  A lot of the other code has already been implemented. Object-oriented-programming is used to create classes and methods. The following files were created:
  - `advanced/database.py` - For initializing the database connection
  - `advanced/cache.py` - Contains the `session_state()` logic
  - `advanced/constants.py` - Contains the table names of the database

💡 Check that everything is running smoothly, if not, contact the teacher/TA!

---

## 4️⃣ Storytelling 📢
Now that the engineering structure is in place, it is time to explore the data further 📊. You have been assigned to a Formula 1 team in pairs, and it is your job to:
- ❓ Give a **presentation** to the management of your team (played by the TA and teacher) on how well you think your team will perform in 2019 based on data from previous years 📈.
- ❓ The CTO (also us) is also interested in learning about the **technical details** of your Streamlit application. Therefore, you should create an extra page in your Streamlit app where you explain how you ensure that your web app stays **fast**, even if the amount of data increases.

Some analytical questions that you should answer in your presentation include:

- ❓ How many points has your team scored over the years?
- ❓ Who are your current drivers?
- ❓ If a driver is not performing well, which drivers from other teams should
your team consider getting?
- ❓ What has historically been the best racetrack for your team? 👍
- ❓ What has been the worst racetrack? 👎
- ❓ Which two teams are your closest competitors? 💥

Use your creativity to come up with additional analysis if you have time. Support your analysis using Streamlit titles and text using Markdown. At the end of the day, we will ask you to present your findings to the group using your Streamlit application 📉. There is no need to create any slides for your presentation. No worries if you do not get to finish all the questions!

🚀 Good luck and enjoy!
