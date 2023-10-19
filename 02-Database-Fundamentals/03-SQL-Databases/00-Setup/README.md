# Setting up Postgres

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D3/postgres-logo.png" alt="drawing" width="200"/>

<br>

Lets start today by setting up our own postgres db on our virtual machine and connecting to it via dbeaver on our local machine!

<br>

### Getting started

We installed postgres and saw that it was running as a service on setup day, but lets check that it is still the case!
```bash
service postgresql status
```
If it is not running:

<details>
<summary markdown='span'>Restart!</summary>

sudo service postgresql restart
</details>


### Interacting from terminal

The simplest way to interact with postgres is with its terminal based front-end: [psql](https://www.postgresql.org/docs/current/app-psql.html)

Let's try connect with just:
```bash
psql
```

You should see an error like this one:

![no db](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D3/psql-no-db.png)

Why? `psql` will try to connect to the database as a postgres user with the same name as your _current linux username_ (to check what what your linux username is, run `echo $USER` or `whoami` from the terminal). We can create a postgres user that matches our linux username to make our workflow as easy as possible!

Luckily, there is a linux user on our virtual machine called "postgres". Let's login as the "postgres" linux user to create our new postgres user. To understand the command below, run `tldr sudo`

```bash
sudo --login --user=postgres psql
```
☝️ we are logging in as the "postgres" user on our linux machine, allowing us to log directly in as the "postgres" user on the database. You should have entered the psql shell from there and should be able to interact with postgres.

👉 **Lets start by creating our own user and password**

For ease, we can create a postgres user with the same username as our linux system username.

```bash
CREATE USER <username> WITH SUPERUSER PASSWORD '<choose a password here>';
# 🚨 Don't forget the ; (semi-column) at the end
# it's mandatory when executing statements in psql
```

☝️ We have created this postgres user a _superuser_, but in general you should try to only assign the appropriate [role attributes](https://www.postgresql.org/docs/current/role-attributes.html) (for example creating a user with the appropriate connection limit to prevent your database being overwhelmed).

👉 Write down your postgres user password in a `.env` file in this challenge folder. We'll need it later on.

```bash
#.env
POSTGRES_PASSWORD='the password you just chose'
```

We now have our postgres user (postgres also provides `createuser` cli but you won't always have direct access to the terminal when using managed postgres solutions).

Now let's log out of postgres (as the _linux_ "postgres" user and postgres "postgres" user) and log back in to postgres as the new user we just created. First we need to exit the current `psql` session:

```bash
\q
```
This `\q` is a special postgres command to shortcut important actions known as [meta commands](https://www.postgresql.org/docs/current/app-psql.html)!

Now we can log back in with our newly created user. Since we created one with our username, we can do:


```bash
psql postgres # which is equivalent to `psql --username=$USER postgres`
```


Let's check our current user with an SQL query
```sql
SELECT current_user;
```

If that query returns the username that we just created, our next step is to create a new database!
```sql
CREATE DATABASE school;
```
If we list the databases, you should see your newly created `school` database. Use the following meta command to list all databases:
```bash
\l
```
Let's connect to the `school` database instead of the default postgres database:
```bash
\c school
```

We can see what tables exist in the `school` database with the following meta command:
```bash
\d
```
None should be returned. Let's create some tables and insert some records in postgres next.


### Creating tables

One way would be with a sql script:
```sql
CREATE TABLE students (
    id          INTEGER PRIMARY KEY,
    first_name  VARCHAR(40) NOT NULL,
    last_name   VARCHAR(40) NOT NULL,
    batch_num   INTEGER
);

INSERT INTO students (
    id
    , first_name
    , last_name
    , batch_num
)
VALUES
      (1, 'Zinedine', 'Zidane', 101)
    , (2, 'Kelly', 'Slater', 101);
```

If you run this query and then run `\d`, you should now see a `students` table appearing, which you can now query:
```sql
SELECT * FROM students;
```

### Dbeaver

While `psql` is very powerful, it would be easier for us to work in a more user focused tool, especially as our queries get more complicated. We'll use [DBeaver](https://dbeaver.io/) as our SQL client - but to get the data from our `postgres` server hosted on virtual machine to DBeaver on our local computer, we need to forward some ports!

First, let's check which port our postgres server is running on (default is 5432) with the following meta command in `psql`:
```bash
\conninfo
```

We need to make that port available on our local machine!

__Step 1:__

In VSCode, click on PORTS next to your TERMINAL section.

![ports tab](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D3/ports-tab.png)

<br>

__Step 2:__

Enter 5432, and press Enter. By default, it auto populates the Local Address section with the value localhost:5432
(if you see a different value then 5432, port 5432 on your local machine is probably occupied by another service - that is totally fine. You can use the local port number of your choice).

At this point, port 5432 on your virtual machine is being forwarded to port 5432 on your local machine.

![forwarded port](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D3/forwarded-port.png)

<br>

__Step 3:__

Open dbeaver and click the new connection button in the top left, then select postgres.

![new conn](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D3/dbeaver-new-conn.png)

<br>

__Step 4:__

Fill out the postgres connection page. Key inputs are in the red boxes:

- database: school
- port: the port you forwarded to
- username: your created user
- password: your created password (check your `.env`!)

<br>

![postgres connection](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D3/postgres-connection.png)

__Step 5:__

You should now see the database on the navigator at the side. Create a script and rerun our original query. You should see the same output as when you ran it in `psql`.

![connected](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D3/connected-dbeaver.png)

### Bringing in data

We are up and running in dbeaver! Time to bring in data from external source. Let's load `teacher.csv` into a new table in our db!

We need to create a table that the teacher data will be inserted into. This table will have 2 columns: `id` - which will be an integer, and `name` - a variable length character type, that we will limit to 50 characters.

The list of all possible Postgres data types is [here](https://www.postgresql.org/docs/current/datatype.html).

Run the following script to create this table:

```sql
CREATE TABLE teachers (
      id      INTEGER
    , name    VARCHAR(50)
);
```

If you run this script again, it should fail with the error: `relation "teachers" already exists`. That is why we generally don’t use the `CREATE TABLE` statement by itself. It is more common to use it with another command depending on the use case.

If we didn't want to overwrite an existing table, we could check to see if the table already exists:
```sql
CREATE TABLE IF NOT EXISTS teachers (
      id      INTEGER
    , name    VARCHAR(50)
);
```

This will not do anything if the table has already been created.

Alternatively, we could fully delete the table and recreate it:
```sql
DROP TABLE IF EXISTS teachers;
CREATE TABLE teachers (
      id      INTEGER
    , name    VARCHAR(50)
);
```

This could be a way to change the table schema.

Let's load the data from the CSV file into the table by running the follow command in `psql`:
```bash
# fist connect to psql
> psql --user=your_db_superuser_name -d school
```
Then run:

<details>
<summary markdown='span'>Quick way to get a full file path!</summary>

```bash
readlink -f <file>
```
</details>

```sql
school=#
\copy teachers
FROM '</home/.../absolute/path/to/teachers.csv>'
DELIMITER ','
CSV HEADER;
```

### Checking the resulting structure of the database

Now that our data has been copied into our tables, it's important to check the global structure of your database. Modern SQL clients enable a clean, high level view of the entirety of your database, with tree-like explorers and other features, but it can be good to confirm with a sql query.

Execute the following in DBeaver to see a list of all columns in every table:
```sql
SELECT *
FROM INFORMATION_SCHEMA.COLUMNS
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position
```

We now have a fully functional postgres database and a workflow when we want to
create new databases and tables!

🏁 🧪 Run `make test` to create test_output.txt. Then git add, commit, and push so your progress is tracked on Kitt!
