After doing the `01-Docker-Compose` exercise, you should by now have a good understanding of a Docker Compose stack, and how to use it to set up a standard web app with a database and a FastAPI web server.

# 0️⃣ Context

### 🎯 Goal
Remember challenge `010401-Tweet-CRUD` where we built a Twitter fast API connected to a postgres service, both running on our linux VM without containers? Well, this time we'll containarize it. But hey, let's spice things up a bit more 🌶

Today we'll build a version of the tweets table **partitioned across two apis**. Indeed, let's imagine our app is struggling to manage the load so we want to create **shards** of the tweets table based on the location of the tweet: Users in Europe can be served their tweets locally and the same in the USA.

This is the architecture we are aiming for:

- Our VM will run **Postgres** as a linux service directly without containers: this will be the full database!
- We'll spawn two **Postgres** containers (two shards EU and US of the full db) with the data volume mapped
- Plus two **FastAPI** app containers for the EU and US database.

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D1/sharded-db.png" width=300>


**Sharding you said ??**  
- When we split a table into several *subsets* that are still part of the same *database*, they are called **partitions**. Partitions are often done by splitting over a particular index (eg. in our case, the user-location column). 
- When we distribute each partitions table into different databases, each partition is a standalone database called a **shard**. 
- When *sharding* or *partitionning*, there is no physical database centralizing all data somewhere anymore! However, we'll still be able to virtually recreate a "full database" in the same way views are just immaterial tables that are created dynamically as you query them. 

**Why sharding?**
- ↔️ Sharding helps us reduce the size of the tables making queries quicker, but can also help us place those tables where they will be accessed (lower latency for users in both regions).
- 🧙‍♀️ You could think of potentially add further sharding in a real case: More locations, or shard by time creation at some point as we expect the most recent tweets to be the most demanded by users!

### Browse `tweets_api` folder rapidly

☝️ Note that it's a simplified version of `010401-Tweet-CRUD`, with much less routes and data complexity.

- Only one model: `Tweet`
- Two routes `get/tweets/` and `post/tweets/`

We'll leave the complexity of routing EU vs. US requests to web developers (Web Browser gives IP address, which can be geo-localized, then routed to EU or US accordingly).  As Data Engineers, we just want to focus on building 2 api containers that connect their respective get/post requests in their respective shard db.

# 1️⃣ Setup postgres on VM

Lets create a new database on our VM for the exercise.

❓ Read again beginning of challenge [01/03/00-Setup/README.md](https://github.com/lewagon/data-engineering-challenges/tree/main/01-Software-Engineering-Best-Practices/03-SQL-Databases/00-Setup#setting-up-postgres) to recall how we created a postgres superuser and password on our VM.

❓ Then, create a database named `tweets` and try to connect to it with DBEAVER
```bash
createdb tweets
```

# 2️⃣ Docker-compose

## 2.1. Networks

❓ In your `docker-compose.yml` add two bridge networks: `europe` &  `usa`.

## 2.2. Databases

❓ In the `docker-compose.yml` create two database postgres services (`us_database`, `eu_database`), one for each network, as below for USA.

<details>
<summary markdown='span'>💡 Example for USA</summary>

```yml
us_database:
  image: postgres:14.2
  restart: on-failure
  healthcheck:
    test: ["CMD", "pg_isready", "-U", "postgres"]
    interval: 5s
    timeout: 5s
    retries: 5
  volumes:
    - ./database/:/docker-entrypoint-initdb.d/
  ports:
    - "5401:5432"
  environment:
    - POSTGRES_PASSWORD=postgres
    - APP_DB_USER=usa
    - APP_DB_PASS=uspassword
    - APP_DB_NAME=ustweets
  networks:
    - usa
```

</details>

💡 Reuse or adjust for EU these different environment variables, forwarded ports and network name as you see fit! You can always change them later on.


## 2.3. APIs

❓ Start the creation of two fastapi services in your docker-compose: `eu_webapi` and `us_webapi` (get inspiration from previous challenge)
- Each should be based on the same `dockerfile-fastapi` that we coded for you
- Each should depend on its respective regional database
- Each should restart on failure
- Each should be only part of their respective regional network
- Each should have POSTGRES_DATABASE_URL equals to the connection string to their regional database
- Each should launch the same command to launch a fastapi server from `tweets_api.main` in port 8000 inside their respective network

**🤔 But how are we we going to differentiate behavior between the US and the EU database then?**

The key is to update the SQLAchemy variable __tablename__ attribute in `model.py` so that it can be set dynamically with an enviroment variable to their respective regional_db_name!
```python
__tablename__ = os.environ.get("TWEETS_TABLE", "tweets")
```

```yml
us_webapi:
  environment:
    - TWEETS_TABLE=us_tweets

eu_webapi:
  environment:
    - TWEETS_TABLE=eu_tweets
```


<details>
<summary markdown='span'>🎁 Solution for US - only look if errors pops up!</summary>

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


## 2.4. Launch

❓ `docker-compose up` and check 🔍:

- `docker ps` should show all 4 containers are up and healthy
- You can connect to the two apis on your local machine 
- You can connect to the 3 DB in Dbeaver

Then we are ready to create our `tweets` main tables and shard it across our other two databases!


# 3️⃣ Sharding

## 3.1 Setup

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

## 3.2. Table creation

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

## 3.3. Connection

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

## 3.4. Edge cases

What about when our systems break and they don't fit in either partion we need somewhere for the overflow to go.

```sql
CREATE TABLE tweets_default
    PARTITION OF tweets
    DEFAULT;
```

# 4️⃣ Testing

Now you can start inserting tweets into the databases and see where the data is avaliable from. For example when you insert into the original tweets table how it becomes avaliable on the foreign server. You can also go the other way and insert into the table on the EU server and query the eu server on the main server with `select * from europe_tweets;`

🏁 This exercise shows the power of using docker compose to test new database architectures quickly without having to launch lots of extra postgres servers on their own hardware!

🤯 You can also use the foreign data wrapper to import other databases once you create the server object:

```sql
IMPORT FOREIGN SCHEMA public
    FROM SERVER <foreign server> INTO public;
```
