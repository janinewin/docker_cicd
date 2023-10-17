## High Level Description

You'll reproduce the steps done in `00-Setup` but with some more complex files.
The goal is to have a database structure ready to then execute SQL queries for  challenges `02-SQL-Basics` and `03-SQL-Advanced`.


# Setup

### **Download [The IMDB Movies Dataset](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/movies_dataset/archive.zip)**

Copy the 2 files into your VM in this challenge's subfolder: `./data/`

    - `movies_metadata.csv`
    - `ratings.csv`

Once locally dowloaded, you can copy them inside your VM via either `scp` (like a pro) or drag-and-drop (thanks to VS code!)

You can quickly explore the dataset on [Kaggle](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset?resource=download&select=ratings.csv) if you want

### **Create a new postgres database called `movies`**, in which we'll later load each CSV in separate tables

A nice shortcut from the command line actually that does the job is:
```bash
createdb "movies"
```

Check that the `movies` table has been created with:
```bash
psql movies # then \l to list your databases and check you are the owner
```

### Lastly, connect it to dbeaver as per previous challenge
And copy your`.env` file from the previous challenge inside this challenge's folder, so you'll be able to run the tests, which will connect to your database.


# `ratings.csv`

## Create the corresponding table `ratings` using SQL commands
- The columns should be named differently than in the CSV (camelCase is not a standard way of naming fields in tables. snake_case is preferred)
    - user_id
    - movie_id
    - rating
    - timestamp
- Choose the correct column types from the list below:
    - `VARCHAR(50)` - when you feel like the length of the data in this field should be limited
    - `TEXT` - when you feel like the length of the data in this field could be big
    - `INT` - if all records in this field seem to be integers that can be stored as 4 bytes (< 2,147,483,647 in absolute term)
    - `BIGINT`- for larger int (8 bytes)
    - `NUMERIC` - if the records may contain decimals
    - `DATE` - self explanatory
- Running the same SQL script again after the table is already created should not fail.

To execute your queries you can either use DBeaver on your local machine, or from `psql` your virtual machines terminal (connect to the `movies` database with `psql movies` 😉)

To explore the structure of the CSV file, you can use bash commands to extract only the first 3 rows (`tldr head`)

🧪 **Write down your query in `ratings_create.sql` when you are done, and test your results with `make test`** (test_2 should pass)

## Load the data from the CSV in the destination table

- Write down your query in `ratings_copy.sql`.
- 💡 The file path to the CSV should be absolute for dbeaver
- ❗️ It should take a while: the file is almost 1GB large and contains more than 26 million rows


## Create a better `timestamp` column
Right now, the timestamp is stored as an "epoch" as `INT` (check what it means online)
We want the date in `TIMESTAMP` to be in a more readable `YYYY-MM-DD HH:MI:SS` format instead!

- Create a new column called `created_at_utc`
- Then, load its converted timestamp equivalent!
- The query should take ~1 minute to run

👉 Write the query in `ratings_update.sql` when you're done.

<details>
  <summary markdown='span'>💡 Hints</summary>

- `ALTER TABLE ... ADD ...` to create a new column
- `UPDATE ... SET ...` to update a column

</details>

<br>


# `movies_metadata.csv`

Let's do the same: create & fill a `movies_metadata` table.

👉 Have a quick look at the CSV structure by printing the first two lines

```shell
cat data/movies_metadata.csv | head -n 2
```

There are 24 columns to manually create, each with its own data type!

Thankfully, there exists nice tools to load CSV automatically


## Create and load automatically with `csvkit`

We have pip-installed for you the amazing [csvkit](https://csvkit.readthedocs.io/en/latest/tutorial/1_getting_started) package (check your `pyproject.toml` file!)

Run the following to let csvkit analyse your CSV to automatically create the long `SQL CREATE TABLE` query for you!

```bash
csvsql -i postgresql data/movies_metadata.csv
```

Now that we have the query, we could copy-paste it in dbeaver and load data as before...But hey, let's make a `bash script` that does this for you!

Copy-paste this script in your terminal, we'll explain it below.

```bash
csv_to_postgres () {
    file_path=$(readlink -f $2)
    table_name=$3

    drop_command="DROP TABLE IF EXISTS ${table_name}"
    psql -d $1 -a -c $drop_command

    tmp=$(mktemp)
    csvsql -i postgresql $2 > $tmp
    psql -d $1 -a -f $tmp

    copy_command="\copy ${table_name} FROM '${file_path}' DELIMITER ',' CSV HEADER"
    psql -d $1 -a -c $copy_command
}
```

🔎 **This is quite a long command so lets break it down!**

It's meant to be run as follows:

```bash
csv_to_postgres movies data/movies_metadata.csv movies_metadata
```
- `$1` `$2` and `$3` are the arguments passed on the command line
  - `$1` db_name
  - `$2` path_to_csv
  - `$3` table_name

- The first part is getting the table name and file path:
  - `readlink -f $2` gets us the absolute file path

- The next part is the drop DB command:
  - Write a SQL command to drop the table if it exists.
  - Then use `psql -d $1 -a -c $drop_command` to execute the command into our database.

- Next, we create the table with our auto generated schema:
  - `tmp=$(mktemp)` creates us a temporary file we can use without having to worry about its cleanup!
  - `csvsql -i postgresql $2` is the most important command. Like when we executed it above, it will generate a schema based on our input csv.
  This command is great on its own, you could use it to generate a schema and work from there to ensure that everything lines up as you expect, but without writing the query manually!
  - We then pipe the output of the previous command to our temporary file `> $tmp`
  - `psql -d $1 -a -f $tmp` is similar to our `psql` command to _drop table if exists_ except that instead of passing a SQL query directly, we are passing a (temporary) file containing a SQL query!

- All that is left to do is copy the data in!
  - Generate a copy command with all the correct variables
  - Execute that into our database `psql -d $1 -a -c $copy_command`

🧪 **Execute the command and test the outcome with `make test`**: test_3 should pass.

🏁 Commit and push your challenge so your progress is tracked on Kitt (don't worry, we 'gitignored' CSVs already).
