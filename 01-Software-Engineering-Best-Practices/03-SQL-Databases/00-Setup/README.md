# Setting up Postgres

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D3/postgres-logo.png" alt="drawing" width="200"/>

<br>

Lets start today by setting up our own postgres db on our virtual machine and connecting to it via dbeaver on our local machine!

<br>

### Getting started

We installed postgres and saw that it was running as a service on setup day but lets check that is still the case!
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

Lets try connect with just:
```bash
psql
```

You should see an error like this one:

![no db](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D3/psql-no-db.png)

The default presumption on psql is that you are trying to connect to a database with the name of your current user (to check this you can run `echo $USER`) and as a postgres user of that name as well, so we need to create a user of that name to make our workflow as easy as possible!

Luckily there is a default user called "postgres": Lets login as the "postgres" user for now. To understand the command below, run `tldr sudo`

```bash
sudo --login --user=postgres psql
```
☝️ we are logging in as the "postgres" user on our linux machine, allowing us to log directly in as the "postgres" user on the database. You should have entered the psql shell from there and should be able to interact with postgres.

👉 **Lets start by creating our own user / password**

The easiest thing to do here is create a user with the same name as your username (`echo $USER` if you forgot).


```bash
CREATE USER <username> WITH SUPERUSER PASSWORD '<choose a password here>';
# 🚨 Don't forget the ; (semi-column) at the end
# it's mandatory when executing statements in psql
```

☝️ We made this user a _superuser_ but in general you should try to only assign the appropriate [role attributes](https://www.postgresql.org/docs/current/role-attributes.html) (for example creating a user with the appropriate connection limit to prevent your database being overwhelmed)

👉 Write down your password in a `.env` file in this challenge folder. We'll need it later on.

```bash
#.env
POSTGRES_PASSWORD='the password you just chose'
```

We now have our user (postgres also provides `createuser` cli but you won't always have direct access to the terminal when using managed postgres solutions).

Now lets log out and log back into the default `postgres` db as our new user.
```bash
\q
```
This `\q` is a special postgres command to shortcut important actions known as [meta commands](https://www.postgresql.org/docs/current/app-psql.html)!

Now we can log back in, with our newly created user because we created one with our username we can do:

bash
```
psql postgres # which is equivalent to `psql --username=$USER postgres`
```


Lets check our current user with a sql query
```sql
SELECT current_user;
```

Now our next step is to create a new database!
```sql
CREATE DATABASE school;
```
If we list the databases you should see your newly created school database
```bash
\l
```
Lets connect to that one instead of the default postgres one:
```bash
\c school
```
If we check the tables in the school db
```bash
\d
```
None should be returned, lets deal with getting data into postgres next.


### Creating tables

The simplest way would be with a simple sql script:
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

If you run this an then run `\d` you should now see a student table appearing which you can now query:
```sql
SELECT * FROM students;
```

### Dbeaver

Before we go further while psql is very powerful it would be easier for us to work in another tool especially as our queries get more complicated.

First lets check which port our postgres server is running on (default is 5432)
```bash
\conninfo
```

We need to make that port available on our local machine!

Step 1:

In VSCode, click on PORTS next to your TERMINAL section.

![ports tab](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D3/ports-tab.png)

<br>

Step 2:

Enter 5432, and press Enter. By default, it auto populates the Local Address section with the value localhost:5432
(if you see a different value then 5432 is probably occupied on your local machine - that's totally fine. You can use the local port number of your choice).

At this point, what it means is
that port 5432 on your virtual machine is forwarded to port 5432 on your local machine.

![forwarded port](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D3/forwarded-port.png)

<br>

Step 3:

Open dbeaver and click the new connection button in the top left and select postgres

![new conn](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D3/dbeaver-new-conn.png)

<br>

Step 4:

Fill out the postgres connection page the key areas are highlighted:

- database: school
- port: the port you forwarded to
- username: your created user
- password: your created password

<br>

![postgres connection](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D3/postgres-connection.png)

Step 5:

You should now see the database on the navigator at the side, then create a script
and rerun our original query and you should see the same output as before.

![connected](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D3/connected-dbeaver.png)

### Bringing in data

Now we are up and running in dbeaver we are ready to deal with our next issue bringing in data from external source. Lets load `teacher.csv` into a new table in our db!


We’re now going to create the table that’s going to welcome the teacher data, which is
made of 2 columns: ID (which is an integer), and name, which is a variable-length variable.
That we will limit to 50 characters. The list of all possible Postgres data types is here
: Data Types. Run the following script to build this structure:

```sql
CREATE TABLE teachers (
      id      INTEGER
    , name    VARCHAR(50)
)
```

Run this script again. It should fail because the relation "teacher" already exists.
That’s why we generally don’t use the CREATE TABLE statement as is.

We either make sure it does not exist already:

```sql
CREATE TABLE IF NOT EXISTS teachers (
      id      INTEGER
    , name    VARCHAR(50)
)
```

which will not do anything if the table has already been created

Or we fully delete the table and recreate it:

```sql
DROP TABLE IF EXISTS teachers;
CREATE TABLE teachers (
      id      INTEGER
    , name    VARCHAR(255)
)
```

which is used when we want to make changes to the structure of the table.

Let’s now load the data from the csv file into the table, by running the following command:

<details>
<summary markdown='span'>Quick way to get a full file path!</summary>

```bash
readlink -f <file>
```

</details>


```bash
# fist connect to psql
> psql --user=your_db_superuser_name -d school
```
Then launch 

```sql
school=# 
\copy teachers 
FROM '</home/..../absolute/path/to/teachers.csv>' 
DELIMITER ',' 
CSV HEADER;
```

Checking the resulting structure of the database

Now that your files are copied into tables in Postgres, you want to check again
what the global structure of your database looks like. Modern SQL clients enable
you to have a pretty clean high level view of the organization of your DB (drop
down menu of all tables, which can be expanded to see the list of columns it contains etc)
but sometimes it is good to check through sql.

Execute this in the SQL query interface:

To see the list of columns in each table

```sql
SELECT *
FROM INFORMATION_SCHEMA.COLUMNS
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position
```

Now we have a fully functional postgres database and a workflow when we want to
create new databases and tables!

🏁 Run `make test` to create test_output.txt, then git add, commit and push so we can track your progress!
