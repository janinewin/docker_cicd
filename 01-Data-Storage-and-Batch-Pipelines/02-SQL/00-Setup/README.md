Note : we encourage you start a new `docker-compose.yml` file from scratch. Rather than reusing the one you did yesterday.

## Setting up Postgres DB

Based on what you've learnt in the previous day, create a brand new `docker-compose.yml`. Add a database system: it will enable you to store data. 

1. Create this service based on the postgres 14 image.
2. Give your container a name : `postgres`. This is optional, but attributing a name to a container brings readibility : it enables you to refer to the container through its name rather than through an ID (Find more documentation about the docker-compose file possible attributes here : [Compose file](https://docs.docker.com/compose/compose-file/))
3. Setup 2 environment variables which will enable you to connect to your database by adding :

    ```yml

    - POSTGRES_DB=db
    - POSTGRES_USER=lewagon

    ```
    
    You don't need to "hide" those credentials, they are not secret.
4. Setup the 3rd environment variable: the password to login to your database.

    ```yml

    - POSTGRES_PASSWORD=$POSTGRES_PASSWORD

    ```

5. This password should be stored somewhere, in a `.env` file at the same level of your `docker-compose.yml`
    - Populate this `.env` file with your actual password, following the format suggested in the `env_template` file.
    - _Why are we doing this ? your `docker-compose.yml` file will eventually be pushed to GitHub. And you don't want any password to be visible so easily in a remote location. So by storing this password in the `.env` file: you're keeping this information locally, since `.env` is ignored by git (check your `.gitignore` file to confirm that this is the case)_
6. Map 2 volumes:
    - the `./data/database/` volume to the `/var/lib/postgresql/data` volume in the docker container. _What is this ? `/var/lib/postgresql/data` in docker contains all the structural files that enable PostGres to work properly. It's interesting for you to see its composition_
    - the `./data/files` volume to the `/files` volume in the docker container. _What is this ? `./data/files` on your local is where you're going to actually store your csv files. Those files need to be copied to the container so that postgres can actually "see" them. And eventually load them in tables. We'll go over this in more details in the section where you actually load files_
7. Let's expose the port so you can directly connect to your postgres database from your local computer (this is needed in order for your tests to run properly): map port `5432` to port `5432` in the docker container.
8. Then add the following `healthcheck` at the same indentation level as the `volumes`

    ```yml
    healthcheck:
      test: [ "CMD", "pg_isready", "-d", "db", "-U", "lewagon" ]
      interval: 5s
      retries: 5
    restart: always
    ```

8. Build and run the docker compose stack

    ```bash
    docker-compose -f docker-compose.yml config
    docker-compose -f docker-compose.yml build
    docker-compose -f docker-compose.yml up
    docker container ls
    docker network ls
    ```

## Setting up Adminer

Now it's time to add a Data Management service: Adminer. It will enable you to execute SQL queries on top of your PostGres database, through a nice interface.

1. Create this service based on the adminer 4.8.1 image. You can check its documentation on https://hub.docker.com/
2. Set the restart policy to `always`
3. Let's expose the port so you can access Adminer from your local computer, and map port `8080` to port `8080` in the docker container.
4. Map the `./data/adminer/` volume to a `/data/` volume in the docker container
5. Build and run the docker compose stack

    ```bash
    docker-compose -f docker-compose.yml config
    docker-compose -f docker-compose.yml build
    docker-compose -f docker-compose.yml up
    docker container ls
    docker network ls
    ```

### (Optional) An alternative to Adminer - Cloudbeaver

Adminer is a database client, it is a friendly interface to your database. There are plenty of such clients, like [DBeaver](https://dbeaver.io/) (free) or [DataGrip](https://www.jetbrains.com/datagrip/) (paid).

An alternative to Adminer that runs in a Docker container and is accessible from a web browser, with a more modern interface, is [Cloudbeaver](https://cloudbeaver.io/). If you find its looks more appealing, feel free to use it instead of Adminer. At the end of the day, they provide the same functionality.

Based on [the Docker documentation](https://github.com/dbeaver/cloudbeaver/wiki/Run-Docker-Container), would you be able to add a section to the Docker Compose to use Cloudbeaver instead or alongside Adminer? If not, the answer is in the hint below.

<details>
  <summary markdown='span'>💡 Hint</summary>

  ```yml
  cloudbeaver:
    image: dbeaver/cloudbeaver:22.1.1
    container_name: cloudbeaver
    restart: always
    volumes:
      # Cloudbeaver user configuration and data is stored in /opt/cloudbeaver/workspace
      # we map this folder to a folder on the server to keep user configuration after a container restart
      - ./data/cloudbeaver/:/opt/cloudbeaver/workspace
    ports:
      # Maps the 8978 port of Cloudbeaver to the server's 8978 port
      # You'll need to add port forwarding from your server's 8978 to your localhost:8978 port using SSH port forwarding 
      - 8978:8978
  ```
</details>

Setting up Cloudbeaver to connect to your Postgres instance is very similar to the Adminer instructions below. So if you decide to pick Cloudbeaver instead of Adminer, just adapt the Adminer instructions to Cloudbeaver's interface. Note that a few things are changing compared to the setup of Adminer : 
-  In CloudBeaver, you'll be asked to setup a `User name` and a `User password` : those have nothing to do with the credentials you setup for Postgres. This is just a protection put in place by CloudBeaver - that asks you to setup / provide credentials to enter the interface.
- Most of the vocabulary is similar to Adminer (although are a bit different), so here's a list of the inputs you'll have to eventually provide :
    - **Driver** : pick `PostgreSQL`
    - **Host** : it's the name of the service in your `docker-compose` file (`postgres`)
    - **Port** : the port to access postgres. Leave it to its default : `5432`
    - **Database** : the name of the db you used in your postgres config in the `docker-compose` (it's one of the `POSTGRES_xxx` variables)
    - **Username** : the username you used in your postgres config in the `docker-compose`
    - **Password**: the password you used in your postgres config in the `docker-compose` 

## Connect to your Postgres database, using Adminer

Let's do a quick recap : your containers are up. The port `8080` on your virtual machine is mapping the port `8080` in the Adminer docker container. Now you want to see the visual interface of Adminer from a web browser, on your local computer. But a firewall is blocking the access to the server. You can bypass this through a method called SSH tunneling (or SSH port forwarding). It allows connections made to a local port (meaning : a port on your own desktop) to be forwarded to a remote machine via a secure channel.

1. In VSCode, click on `PORTS` next to your `TERMINAL` section (Step 1 screenshot below). Hit "Forward a Port". Enter `8080`, and press `Enter`. By default, it auto populates the `Local Address` section with the value `localhost:8080`. At this point, what it means is that port `8080` on your local computer is forwarded to port `8080` on your VM. In order for us to distinguish a bit more all those ports (and not have them all equal to `8080`), let's change the `Local Address` : Right click on it > "Change Local Address Port" > `8082` (Step 2 screenshot below)

    _Step 1_

    <img src='https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D2/port_forwarding_1.png' width=500>

    _Step 2_

    <img src='https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D2/port_forwarding_2.png' width=500>

    Now : from your local machine, on port `8082`, you'll be able to access port `8080` on your VM, which will be able to access port `8080` on the Adminer container, which can access the postgres container because they're part of the same Docker network. An illustrated version of this can be found in the Networking / Port mapping section of the [CHEATSHEET.md](https://github.com/lewagon/data-engineering-challenges/blob/main/CHEATSHEET.md)

2. Now connect to your PostGres instance from Adminer. Open a Chrome window and enter the URL: http://localhost:8082. It should bring you to the Adminer welcome page.
3. You will be prompted for a couple of inputs:
    - **System**: it's a drop down menu. Guess what system you're interacting with
    - **Server**: it's the name of the service in your `docker-compose` file
    - **Username**: the username you used in your postgres config in the `docker-compose`
    - **Password**: the password you used in your postgres config in the `docker-compose`
    - **Database**: the name of the db you used in your postgres config in the `docker-compose` (it's one of the `POSTGRES_xxx` variables)

You should now be connected to the Postgres DB, from the Adminer interface!

## Play around with the interface

In the `public` schema, you're going to create 2 tables:
- Create 1 by using the _Create table_ feature. It enables you to manually create a table, name the columns it's made of, as well as specify their types.
- Create 1 by using the _SQL command_ feature. Through a SQL script, you'll be able to create the structure of the table, as well as populate it. Just copy paste the script below:

    ```sql
    CREATE TABLE student (
        id          INTEGER PRIMARY KEY,
        first_name  VARCHAR(40) NOT NULL,
        last_name   VARCHAR(40) NOT NULL,
        batch_num   INTEGER
    );

    INSERT INTO student (
        id
        , first_name
        , last_name
        , batch_num
    )
    VALUES
        (1, 'Zinedine', 'Zidane', 101)
      , (2, 'Kelly', 'Slater', 101);
    ```

- The _Import_ feature does not allow you to import csv files from your local computer. To import your `movies` dataset, we need a workaround: loading it through a script (which in any case would be needed, since we should never load data in such a manual way)

## Storing data into Postgres

We now want to do the following setup:
- Having csv files on a local machine
- Have those csv files propagated to our Postgres container (so the container "sees" them)
- Load the data of this csv into a table
- Select data from that table using Adminer

We'll do it on a very simple file - and you'll have to do it yourself with the movies dataset

### Porting local csv files to our postgres container

1. After your containers are up, the `adminer` and `postgres` services should have created, on your local machine, 2 folders under the `./data` folder:
    - `/adminer` (Adminer file system)
    - `/database` (Postgres DB). This folder contains "system" folders for PostGres to work properly. What we need is a place where we would store the csv files from the movies dataset. Which would then be loaded in tables in Postgres
2. To do so, create a folder `/files` under the `./data` folder.
3. Move the `teacher.csv` file that's under `02-SQL/00-Setup/` to `02-SQL/00-Setup/data/files/`
4. Kill your container, and relaunch it:

    ```bash
    docker-compose -f docker-compose.yml up
    ```

5. Double check that your postgres container can indeed see this `teacher.csv` file:

    ```bash
    $ docker exec -it postgres /bin/bash
    $ ls
    # should return a bunch of folders, including "files"
    $ ls files
    # should return teacher.csv
    ```

### Load the data in the csv into a PostGres table

1. Go to Adminer interface, and to the "SQL command" section
2. We're now going to create the table that's going to welcome the teacher data, which is made of 2 columns: ID (which is an integer), and name, which is a variable-length variable. That we will limit to 50 characters. The list of all possible Postgres data types is here: [Data Types](https://www.postgresql.org/docs/9.1/datatype.html). Run the following script to build this structure:

    ```sql
    CREATE TABLE teacher (
        id      INTEGER
    , name    VARCHAR(50)
    )
    ```

3. Run this script again. It should fail because the `relation "teacher" already exists`. That's why we generally don't use the `CREATE TABLE` statement as is.
    - We either make sure it does not exist already:

        ```sql
        CREATE TABLE IF NOT EXISTS teacher (
            id      INTEGER
        , name    VARCHAR(50)
        )
        ```

    which will not do anything if the table has already been created
    - Or we fully delete the table and recreate it:

        ```sql
        DROP TABLE IF EXISTS teacher;
        CREATE TABLE teacher (
            id      INTEGER
        , name    VARCHAR(255)
        )
        ```

    which is used when we want to make changes to the structure of the table.
    - Let's now load the data from the csv file into the table, by running the following command:

        ```sql
        COPY teacher
        FROM '/files/teacher.csv'
        DELIMITER ','
        CSV HEADER
        ```

### Checking the resulting structure of the database

Now that your files are copied into tables in Postgres, you want to check again what the global structure of your database looks like. Modern SQL clients enable you to have a pretty clean high level view of the organization of your DB (drop down menu of all tables, which can be expanded to see the list of columns it contains etc). Adminer does not have such a clean interface, but you can still have a high level view through SQL statements:

Execute this in the SQL query interface:
- To see your list of tables in the DB

    ```sql
    SELECT *
    FROM INFORMATION_SCHEMA.TABLES
    WHERE table_schema = 'public'
    ```

- To see the list of columns in each table

    ```sql
    SELECT *
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE table_schema = 'public'
    ORDER BY table_name, ordinal_position
    ```

- Wondering how to determine what can be queried in this structural `INFORMATION_SCHEMA` database ? They are still tables, but in a `table_schema` that's different from `public`, so this does the job:

    ```sql
    SELECT *
    FROM INFORMATION_SCHEMA.TABLES
    WHERE table_schema = 'information_schema'
    ```
