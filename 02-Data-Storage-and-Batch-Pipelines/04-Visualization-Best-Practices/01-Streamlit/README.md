## Background
In this exercise we'll setup a simple PostgreSQL, Adminer, [Streamlit](https://streamlit.io/) stack using docker compose.
The new tool we are introducing, Streamlit is a convenient python solution to create simple UI to showcase data from various sources.
It can be used to present data into custom dashboards, or simply used to create a python web app.


## End Goal
By the end of this exercise you should:
- Have a working stack using docker-compose (PostgreSQL, Adminer, Streamlit)
- Have The Formula 1 database loaded into PostgreSQL
- Be able to check out [http://localhost:8501](http://localhost:8501) and see the welcome message

## Exercise
1. As usual, run the `make install` at the root directory of this exercise to add all the necessary dependencies and download the necessary content for the day

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
- with command : `["streamlit", "run", "run.py"]` this small script allows us to run streamlit along with our future modules
- Opening the port 8501
- Depending on the database service

6. Head to http://localhost:8501 👉 you should see the welcome service ✨


## Data
We are going to use real Formula 1 data. The goal of this exercise is to get you familiar with the basic functionality of Streamlit, while exploring the Formula 1 dataset.

## Streamlit basics
In the `app` folder there is a file called `main.py`. It is already
partly filled with code, but your goal is to enhance the main Streamlit page
with the following:
- Add the right caching decorator to the `load_data` function
- Create a Streamlit title, subheader on the main page. Do the same in the sidebar
- The data that is loaded needs to be saved into the session state for it
to be reusable across different pages in Streamlit
- In the pages subdirectory, create two Python files. See the Streamlit documentation
for more info on how this works. Create one file for doing descriptive
statistics, and another one for visualizing the data. It is up to you to decide
on the data that you want to visualize. Create something cool!
