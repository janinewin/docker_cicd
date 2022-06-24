# Week 1 Day 5: Visualization and Best Practices

## Background
In this exercise we'll setup a simple PostgreSQL, Adminer, [Streamlit](https://streamlit.io/) stack using docker compose.
The new tool we are introducing, Streamlit is a convenient python solution to create simple UI to showcase data from various sources.
It can be used to present data into custom dashboards, or simply used to create a python web app.


## End Goal
By the end of this exercise you should:
- Have a working stack using docker-compose (PostgreSQL, Adminer, Streamlit)
- Have The Formula 1 database loaded into PostgreSQL
- Be able to check out http://localhost:8501 and see the welcome message

## Exercise
1. Run the make install target at the root directory of this exercise to add all the necessary dependencies and download the necessary content for the day

2. In the docker-compose file - Create the database service:
- based on PostgreSQL 14
- with a Restart policy: `Always`
- Loading the database f1db.sql located in `database/init/f1db.sql` into PostgreSQL leveraging volumes and the image's entrypoint `/docker-entrypoint-initdb.d/`
- witht the Environment variables:
```
      - POSTGRES_DB=f1db
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_USER=postgres
```


4. Create the adminer service:
- Open the ports 8080
- with a Restart policy: `Always`
- Depending on the database service

5. Create the Streamlit service
- Building the image located at the root folder
- with a Restart policy: `Always`
- Mounting the root folder into `/app/`
- Mounting the `./.streamlit` folder into `/app/.streamlit/`
- with command : `["streamlit", "run", "run.py"]` this small scripts allows us to run streamlit along with our future modules
- Opening ports 8501
- Depending on the database service

6. Head to http://localhost:8501  you should see the welcome service
