## High Level Description

You'll reproduce the steps done in `00-Setup` but with some more complex files.
The goal is to have a database structure ready to then execute SQL queries on it in the challenges `02-SQL-Basics`, `03-SQL-Advanced` sections.


# 1️⃣ Setup

### 1) **Download [The IMDB Movies Dataset](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/movies_dataset/archive.zip)**

Copy the 2 files into your VM in this challenge's subfolder: `./data/`  

    - `movies_metadata.csv`
    - `ratings.csv`

💡 Once locally dowloaded, you can copy them inside your VM via either `scp` (like a pro) or drag-and-drop (thanks to VS code!)

💡 You can quickly explore the dataset on [Kaggle](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset?resource=download&select=ratings.csv) if you want

### 2️) **Create a new postgres database called `movies`**, in which we'll later load each CSV in separate tables

💡 A nice shortcut actually does the job is
```bash
createdb "movies"
```

Check that it worked with
```bash
psql movies # then \l to list your databases and check you are the owner
```

### 3) Lastly, connect it to DBEAVER as per previous challenge
And copy your`.env` file from the previous challenge inside this challenge's folder, so you'll be able to run the tests, which will connect to your database.


# 2️⃣ `ratings.csv`

## 2.1) Create the corresponding table `ratings` using SQL commands
- The columns should be named differently than in the csv (camelCase is not a standard way of naming fields in tables. snake_case is preferred)
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
- Running the same SQL script again after the table is already created should not fail

💡 To execute your queries, you can either use local DBEAVER connection, or your terminal running `psql movies`

💡 To explore the structure of the CSV file, you can use bash commands to extract only the first 3 rows (`tldr head`)

🧪 **Write down your query in `ratings_create.sql` when you are done, and test your results with `make test`** (test_2 should pass)

## 2.2) Load the data from the csv in the destination table

- Write down your query in `ratings_copy.sql`.
- 💡 The file path to the CSV should be absolute for DBEAVER
- ❗️ It should take a while: the file is almost 1GB large and contains more than 26 million rows


## 2.3) Create a better `timestamp` column
Right now, timestamp is stored as an "epoch" as `INT` (check what it means online)
We want date in `TIMESTAMP` in more readable `YYYY-MM-DD HH:MI:SS` format instead!

- Create a new column called `created_at_utc`
- Then, load its converted timestamp equivalent!
- The query should take ~1 minute to run

👉 Write the code in `ratings_update.sql` when you're done

<details>
  <summary markdown='span'>💡 Hints</summary>

- `ALTER TABLE ... ADD ...` to create a new column
- `UPDATE ... SET ...` to update a column

</details>

<br>


# 3️⃣ `movies_metadata.csv`

Let's do the same: create & fill a `movies_metadata` table.

👉 Have a quick look at the CSV structure by printing the first two lines

```shell
cat data/movies_metadata.csv | head -n 2
```

🤯 There are 24 columns to manually create, each with its own data type!

Hopefully, there exists nice tools to load CSV automatically


## 3.1) create and load automatically with `csvkit`

We have pip-installed for you the amazing [csvkit](https://csvkit.readthedocs.io/en/latest/tutorial/1_getting_started) package (check your `pyproject.toml` file !)

Run the following to let csvkit analyse your CSV to create the long SQL CREATE TABLE query automatically for you!

```bash
csvsql -i postgresql data/movies_metadata.csv
```

Now that we have the query, we could copy-paste it in DBEAVER and load data as before...But hey, let's make a script that automatically does this for you! 🎭

Copy-paste this script in your terminal, we'll explain it below

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

It's meant to be run as follow:

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
  - Write a sql command to drop the table if it exists
  - Then use `psql -d $1 -a -c $drop_command` to execute the command into our database

- Next we create the table with our auto generated schema:
  - `tmp=$(mktemp)` creates us a temporary file we can use without having to worry about its cleanup!
  - `csvsql -i postgresql $2` is the most important command here this will generate us a schema based on our input csv. This command is great on its own if you want to use it to generate a schema and work from there to audit that everything lines up as you expect but without manually working through everything!
  - We then pipe that to our temporary file `> $tmp`
  - `psql -d $1 -a -f $tmp` this is similar to our command from dropping except that instead of passing a sql query directly we are passing it a file containing a sql query!

- All that is left to do is copy the data in!
  - Generate a copy command with all the correct variables
  - Execute that into our database `psql -d $1 -a -c $copy_command`

🧪 **Execute the command and test the outcome with `make test`**: test_3 should pass.

🏁 Commit and push your challenge so we can keep track of your progress (don't worry, we 'gitignored' csvs already)
