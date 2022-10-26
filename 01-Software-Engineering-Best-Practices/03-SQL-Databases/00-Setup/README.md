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

The default presumption on psql is that you are trying to connect to a database with the name of your current user and as a postgres user of that name as well!

Luckily there is a default user the postgres user so lets login as the postgres user for now.
```bash
sudo --login --user=postgres psql
```

You should enter the psql shell from here you can interact with postgres. Lets start by creating our own user the easiest thing to do here is create a user with the same name as your username. Here we are makeing the user a superuser but in general you should try to only assign the appropriate [role attributes](https://www.postgresql.org/docs/current/role-attributes.html) (for example creating a user with the appropriate connection limit to prevent your database being overwhelmed):

```bash
CREATE USER <username> WITH SUPERUSER PASSWORD '<your password>';
```

The most important thing when executing statements in psql is terminating them with the semicolon `;`!
We now have our user (postgres also provides `createuser` cli but you won't always have direct access to the terminal when using managed postgres solutions).

Now lets log out and log back into the default `postgres` db as our new user.
```bash
\q
psql postgres
```
Check our current user with a sql query
```sql
SELECT current_user;
```

Now our next step is to create a new database!
```sql
CREATE DATABASE public;
```
If we list the databases you should see your newly created public database
```bash
\l
```
Lets connect to that one instead of the default postgres one:
```bash
\c public
```
If we check the tables in the public db
```bash
\d
```
None should be returned, lets deal with getting data into postgres next.


### Creating tables

The simplest way would be with a simple sql script:
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

If you run this an then run `\d` you should now see a student table appearing which you can now query:
```sql
SELECT * FROM student;
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
(if you see a different value then 5432 is probably occupied on your local machine). At this point, what it means is
that port 5432 on your virtual machine is forwarded to port 5432 on your local machine.

![forwarded port](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D3/forwarded-port.png)

<br>

Step 3:

Open dbeaver and click the new connection button in the top left and select postgres

![new conn](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D3/dbeaver-new-conn.png)

<br>

Step 4:

Fill out the postgres connection page the key areas are highlighted:

- database: public
- port: the port you forwarded to
- sername: your created user
- password: your password

<br>

![postgres connection](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D3/postgres-connection.png)

Step 5:

You should now see the database on the navigator at the side, then create a script
and rerun our original query and you should see the same output as before.

![connected](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D3/connected-dbeaver.png)

### Bringing in data

Now we are up and running in dbeaver we are ready to deal with our next issue bringing in data from sources
other inserting with a sql query. Lets load `teacher.csv` into a new table in our db!


We’re now going to create the table that’s going to welcome the teacher data, which is
made of 2 columns: ID (which is an integer), and name, which is a variable-length variable.
That we will limit to 50 characters. The list of all possible Postgres data types is here
: Data Types. Run the following script to build this structure:

```sql
CREATE TABLE teacher (
      id      INTEGER
    , name    VARCHAR(50)
)
```

Run this script again. It should fail because the relation "teacher" already exists.
That’s why we generally don’t use the CREATE TABLE statement as is.

We either make sure it does not exist already:

```sql
CREATE TABLE IF NOT EXISTS teacher (
      id      INTEGER
    , name    VARCHAR(50)
)
```

which will not do anything if the table has already been created

        Or we fully delete the table and recreate it:

```sql
DROP TABLE IF EXISTS teacher;
CREATE TABLE teacher (
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


```sql
COPY teacher
FROM '<path to teachers.csv>'
DELIMITER ','
CSV HEADER
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

This can be a slightly tedious so there are some tools (like [csvkit](https://csvkit.readthedocs.io/en/latest/))
which aim to streamlit the csv -> database workflow.

### Bonus

Script to automate the process using csvkit (installed with pipx)!

```bash
csv_to_postgres () {
    file_path=$(readlink -f $2)
    table_name=$(echo $2 | sed 's:.*/::')
    table_name="${table_name%.*}"
    tmp=$(mktemp)

    drop_command="DROP TABLE IF EXISTS ${table_name}"
    psql -d $1 -a -c $drop_command

    csvsql -i postgresql $2 > $tmp
    psql -d $1 -a -f $tmp

    copy_command="COPY ${table_name} FROM '${file_path}' DELIMITER ',' CSV HEADER"
    psql -d $1 -a -c $copy_command
}
```
