# Basic Docker stack

After doing the `01-Docker-Compose` exercise, you should by now have a good understanding of a Docker Compose stack, and how to use it to set up a standard web app with a database and a FastAPI web server.

## Desired outcome

🏁 We want to reuse our skills to help us build a versions of the tweets table partitioned across two apis. Our app is struggling to manage the load so we want to create shards of the tweets table based on the location of the tweet, so that users in Europe can be served their tweets locally and the same in the USA.

- Our vm running **Postgres** this will be the base database!
- Two **Postgres** containers with the data volume mapped, and environment variables set up.
- Two **FastAPI** app containers for the EU and US database.

This is the architecture we are aiming for:

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D1/sharded-db.png" width=700>

Once we can shard to these two regions we could potentially add further sharding. Sharding helps us reduce the size of the tables making queries quicker but can also help us place those tables where they will be accessed (lower latency for users in both regions). In this case by location but we might also shard by time creation at some point as we expect the most recent tweets to be the most demanded by users!

## 1️⃣ Setup

First lets create a new database on our vm for the exercise.

```bash
createdb tweets
```

Then connect with dbeaver to your new database.


## 2️⃣ Docker-compose


### 2.1. Networks

❓ In your `docker-compose.yml` add two bridge networks: `europe` &  `usa`.

### 2.2. Databases

❓ In the `docker-compose.yml` create a databases for each network you can reuse the differences being enviroment variables, forwarded ports, network, and service name!

<details>
<summary markdown='span'>💡 Example for USA</summary>

```yml
us_database:
  image: postgres:14.2
  restart: on-failure
  healthcheck:
    test: ["CMD", "pg_isready -U postgres"]
    interval: 5s
    timeout: 5s
    retries: 5
  volumes:
    - ./database/:/docker-entrypoint-initdb.d/
  ports:
    - "5401:5432"
  environment:
    - POSTGRES_USER=postgres
    - POSTGRES_PASSWORD=postgres
    - APP_DB_USER=usa
    - APP_DB_PASS=uspassword
    - APP_DB_NAME=ustweets
  networks:
    - usa
```

</details>

### 2.3. APIs

Time to add api services to docker-compose, create two more services in your docker-compose
launching the `tweets_api` fastapi. The first step is to go to `model.py` and **update the tablename attribute so that it can be set dynamically with an enviroment variable.**

<details>
<summary markdown='span'> Tablename solution</summary>

```python
__tablename__ = os.environ.get("TWEETS_TABLE", "tweets")
```

</details>


❓ Now write the services for the two fastapis the key parts to add here are the enviroment variables:

- POSTGRES_DATABASE_URL=the connection to the database
- TWEETS_TABLE=the name of the table here because we are going to be sharding it should help identify the shard. For example `us_tweets` for the us section of the tweets!

<details>
<summary markdown='span'>Example for US fastapi</summary>

```yml
us_webapi:
  container_name: us_api
  build:
    context: .
    dockerfile: dockerfile-fastapi
  restart: on-failure
  ports:
    - "8001:8000"
  volumes:
    - ./tweets_api:/app/tweets_api
  environment:
    - POSTGRES_DATABASE_URL=postgresql+psycopg2://usa:uspassword@us_database:5432/ustweets
    - TWEETS_TABLE=us_tweets
  command: ["uvicorn", "tweets_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
  networks:
    - usa
  depends_on:
    - us_database
```

</details>


### 2.4. Launch

❓ `docker-compose up` and connect to the two apis to check they are running. Make sure you can connect to all three dbs through dbeaver then we are ready to create our database and shard it across our other two databases!


## 3️⃣ Sharding

### 3.1 Setup

Our first call on our host database is to activate the postgres foreign data wrapper extension. This allows us to use new functions to access SQL data on other servers.
```sql
CREATE EXTENSION postgres_fdw;
```

Lets connect to our foreign server (in this example europe). Here **take care for the dbname and port** depending on what you defined in your compose file! This creates a new SQL object called a server.
```sql
CREATE SERVER europe FOREIGN DATA WRAPPER postgres_fdw
    OPTIONS (host '127.0.0.1', port '5400', dbname 'eutweets');
```

Now login in to the server. Here in the example I want my current user "oliver.giles" to be able to execute SQL on the foreign server `europe` as the user `europe` and I also give the password. This means when I am connected to the host database as the `oliver.giles` user I can execute SQL on the europe server SQL database as well ❗️
```sql
CREATE USER MAPPING FOR "oliver.giles" SERVER europe
    OPTIONS (user 'europe', password 'eupassword');
```

### 3.2. Table creation

We need to create a new table **on the host machine** and add a new call `partion by` which describes how the database will be seperated. In this case by the `string` appearing in the location column.
```sql
CREATE TABLE tweets (
	id serial4 NOT NULL,
	"location" varchar NOT NULL,
	"text" varchar NOT NULL,
	owner_id int4 NOT NULL,
	like_count int4 NOT NULL
) partition by list ("location");
```

**Logged into the european server** we need to create a table with matching columns!

```sql
CREATE TABLE europe_tweets (
	id serial4 NOT NULL,
	"location" varchar NOT NULL,
	"text" varchar NOT NULL,
	owner_id int4 NOT NULL,
	like_count int4 NOT NULL
);
```

We are now ready to use the SERVER object we created to connected the master table to this foreign partion.

### 3.3. Connection

**On our host server** lets connect the two and define the values which should be fed into the european partion. So here when `europe` is the string in the `location` column it should be stored in this partion!

```sql
CREATE FOREIGN TABLE europe_tweets
    PARTITION OF tweets
    FOR VALUES IN ('europe')
    SERVER europe;
```

Lets repeat that for the us!

1. Create the table on the US server.

```sql
CREATE TABLE us_tweets (
	id serial4 NOT NULL,
	"location" varchar NOT NULL,
	"text" varchar NOT NULL,
	owner_id int4 NOT NULL,
	like_count int4 NOT NULL
);
```

2. Create the connection !

```sql
CREATE SERVER usa FOREIGN DATA WRAPPER postgres_fdw
    OPTIONS (host '127.0.0.1', port '5401', dbname 'ustweets');
CREATE USER MAPPING FOR "oliver.giles" SERVER usa
    OPTIONS (user 'usa', password 'uspassword');
CREATE FOREIGN TABLE us_tweets
    PARTITION OF tweets
    FOR VALUES IN ('usa')
    SERVER usa;
```

### 3.4. Edge cases

What about when our systems break and they don't fit in either partion we need somewhere for the overflow to go.

```sql
CREATE TABLE tweets_default
    PARTITION OF tweets
    DEFAULT;
```

## 4️⃣ Testing

Now you can start inserting tweets into the databases and see where the data is avaliable from. For example when you insert into the original tweets table how it becomes avaliable on the foreign server. You can also go the other way and insert into the table on the EU server and query the eu server on the main server with `select * from europe_tweets;`

🏁 This exercise shows the power of using docker compose to test new database architectures quickly without having to launch lots of extra postgres servers on their own hardware!

🤯 You can also use the foreign data wrapper to import other databases once you create the server object:

```sql
IMPORT FOREIGN SCHEMA public
    FROM SERVER <foreign server> INTO public;
```
