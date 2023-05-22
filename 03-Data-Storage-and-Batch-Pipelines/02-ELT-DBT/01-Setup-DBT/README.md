# 🎯 Goals

There are 5 steps in this setup
1. Setup Big Query
1. Install DBT
2. Build a DBT project (folder structure + config file)
3. Setup the connection configuration with BigQuery (profile file)
4. Run your first DBT models, which will generate *tables* and *views* in BigQuery

# 1️⃣ Setup Big Query

BigQuery enables you to query data stored in different locations / projects. In this challenge, we'll be interacting with 2 projects :
- The project where the source data is stored. It's a project made public by Google to enable Data Scientists to play around with data. The project is called `bigquery-public-data`, and the name of the dataset is `hacker_news`
- Your own project, that you created during the Data Engineering Setup.

Let's pin those 2 in the BigQuery interface.

1. Go to the BigQuery interface [here](https://console.cloud.google.com/bigquery)
   
2. Star the `bigquery-public-data` project so you can more easily interact with it : Click on **ADD DATA > Star a project by name**, type : `bigquery-public-data`. Hit **STAR**
   
3. Do the same thing with your own project : in the example / screenshot below, the "personal" project is called `ingka-data-engineering-dev`
   
4. Your BigQuery interface should now look like this (except that instead of `ingka-data-engineering-dev`, it will be your project name):

<img src='https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W2D1/bigquery_interface_final.png' size=200>

# 2️⃣ Install DBT

- There are multiple versions of DBT, which vary depending on the database system you're interacting with. In our case, we're using BigQuery. You'll thus be installing `dbt-bigquery`. Make sure it's part of the packages included in `pyproject.toml`, and run `poetry install` in the `01-Setup-DBT` folder to install it.
- Make sure DBT is indeed installed by executing `dbt --version` in your terminal.

# 3️⃣ Initialize the DBT project

## Initialize `dbt_lewagon` folder

- In your terminal, go at current-challenge root. This is where we'll create the DBT project.
- Once there, you need to init (create the folder structure) of the DBT project - we'll call it `dbt_lewagon`.
- In command lines, run `dbt init`. When prompted:
  - _Enter a name for your project (letters, digits, underscore)_ Enter: `dbt_lewagon`. If prompted : _The profile dbt_lewagon already exists in ~/.dbt/profiles.yml. Continue and overwrite it?_ Hit `N`.
  - _Which database would you like to use? Enter a number:_ Enter : `1` (for `bigquery`)
  - _Desired authentication method option (enter a number):_ Enter: `2` (for `service_account`)
  - _keyfile (/path/to/bigquery/keyfile.json):_ : Enter the absolute path of where you stored your BigQuery service account key (that you created during the Data Engineering setup, [here](https://github.com/lewagon/data-engineering-setup/blob/main/macOS.md)), including the file name and its extension. Meaning it should look something like this :  `/home/username/code/.gcp_keys/le-wagon-de-bootcamp.json` (If you spell it wrong, you'll be able to modify it later).
  - _project (GCP project id)_ : Self explanatory : Enter your Google Cloud project ID (that you created during the Data Engineering setup, [here](https://github.com/lewagon/data-engineering-setup/blob/main/macOS.md))
  - _dataset (the name of your dbt dataset)_ : Please be cautious here. Call it `dbt_{firstletteroffirstname}{last_name}_day1` hence if your name is Barack Obama, your dataset should be `dbt_bobama_day1`.
  - _threads (1 or more)_ : Enter `1`
  - _job_execution_timeout_seconds [300]_ : Enter `300`
  - _Desired location option (enter a number):_ : Enter `1` for `US`. This is important : the dataset we'll be exploring is located in the US - it facilitates things if you set up a "receiving" dataset that's also in the US.

This should have done 2 things
- It generated all the tree structure needed for the DBT project under the `dbt_lewagon` folder
- It should have created a `profiles.yml` file at the following location : `~/.dbt/profiles.yml`

## Verify the setup of `profiles.yml`

_High level info (no action item) : the section relates to the DBT profile. 1 DBT project maps to 1 DBT profile, which generally maps to 1 company. Typically as a Le Wagon teacher, in my `profiles.yml` I have 2 profiles : 1 for LeWagon, 1 for the company I work at. The Le Wagon profile can write to several "targets" : 1 target corresponds to a location where the profile can insert some data. Hence, each target is associated to a Data Warehouse system (BigQuery, Redshift etc), credentials with certain accesses, a location for the target (where the data will be inserted / in which dataset ? etc)_

_For more information about the DBT profile, you can read this documentation:_
- _[`profiles.yml`](https://docs.getdbt.com/reference/profiles.yml)_
- _[BigQuery profile](https://docs.getdbt.com/reference/warehouse-profiles/bigquery-profile)_

Let's check that the `profiles.yml` file is configured correctly :
- Your DBT profile should be stored in a folder at your root called `.dbt`. Open it by running : `code ~/.dbt/profiles.yml`. You should be able to see all the configuration you've set when creating the DBT project.
- Run `make test` to make sure the setup of your profile is correct. (The `test_dbt_profile` tests should all be green). Watch out with the levels of indendation in your `profiles.yml` file
- Push to git.

### Verify `dbt_project.yml` file

_No action item in this section - we're just providing context._

- Open the `dbt_lewagon` folder, and open the `dbt_project.yml` file in this folder:
  - Verify that the project name is correct : `name: 'dbt_lewagon'`
  - Verify that the profile name is correct : `profile: 'dbt_lewagon'`
  - At the bottom of the file, change, make sure the `models` parameter refers to your project name:
  ```yml
  models:
  dbt_lewagon:
    # Config indicated by + and applies to all files under models/example/
    example:
      +materialized: view
  ```
    What is this ? You're basically saying that by default, your models DBT created in BigQuery should be `views`. Unless you specifically specify something else when configuring a model (making it a `table`, or an `incremental` model for example).

### Verify initial tree structure of the DBT project

_No action item in this section - we're just providing context._

- First, make sure that in the `models` folder, you can find 2 files :
  - `/example/my_first_dbt_model.sql`
  - `/example/my_second_dbt_model.sql`
  - Check how the configuration of those models is built
    - `my_first_dbt_model.sql` is generating some fake `source` data, through a CTE. And is then storing this result in a `table` (see the config, that's where you decide the output should be a table), called `my_first_dbt_model` (it uses the name of the file)
    - `my_second_dbt_model.sql` is based / refers to the `my_first_dbt_model` model. The materialization is not specified : there's no configuration section : it will be stored as a view, since - as explained above - this is the default materialization we're using in the `dbt_project.yml`.
- Let's explore the `/models/example/schema.yml` file. In there you can find
  - The list of models in the folder
  - A high level description of each model
  - For each column of each model, the ability to document
    - its description
    - its constraints (unicity, the field not being null etc).

# 3️⃣ Enhance DBT project tree

**From now on, all command lines assume you're executing them from your `dbt_lewagon` directory**

Let's organize the project better. We said there are 3 layers :
- the `source` data
- the `staging` data - which is cleaner version of the `source` data
- the `mart` data - which contains clean metrics business stakeholders can report on.

Let's make sure the `.sql` file corresponding to each layer lie in a folder that corresponds to what they're supposed to do: `cd` to the `dbt_lewagon` directory. From there, execute the following command :

  ```bash
    mkdir models/source;
    mkdir models/staging;
    mkdir models/mart;
  ```

### Re organise macros

Macros are pieces of reusable code which work like functions in Python. They take inputs, give an output, and can be used throughout the models of your project. To enable this, let's restructure the `macros` folder. From the `dbt_lewagon` directory : execute the following command :

```bash
mkdir macros/meta;
mkdir macros/models;
```
- `meta` macros will be used for project / architecture related functions (like the one we mentioned above)
- `models` macros will be used for functions automating some parts of specific models.

 We built the above structure (`mart` and `staging` folders) for a specific reason : we want `.sql` models
- saved under the `staging` folder to create schemas in the BigQuery project that easily identify them, with a prefix `stg_`
- saved under the `mart` folder to create schemas in the BigQuery project that easily identify them, with a prefix `mart_`

### Let's make sure your structure is correct

Your DBT project structure should now look like this (`target` may or may not have sub directories, depending on whether you've already run some models - don't worry too much about that directory)
```
.
├── README.md
├── analyses
├── data
├── dbt_project.yml
├── macros
│   ├── meta
│   └── models
├── models
│   ├── example
│   │   ├── my_first_dbt_model.sql
│   │   ├── my_second_dbt_model.sql
│   │   └── schema.yml
│   ├── mart
│   ├── source
│   └── staging
├── snapshots
└── tests
```

# 4️⃣ Run your first models and tests 🧪

Your setup is now ready to run your first models.
- Execute the following command to generate your models :
  - `dbt run -m my_first_dbt_model`
    If you've understood well the instructions : do you know where this model will be created in BigQuery ?
  - `dbt run -m my_second_dbt_model`
  - `my_second_dbt_model` is dependent on `my_first_dbt_model`. If you want to refresh `my_second_dbt_model` having `my_first_dbt_model` being refreshed first, run the following command :
     `dbt run -m +my_second_dbt_model`
- As seen in `dbt_lewagon/models/example/schema.yml` :
  - `id` in `my_first_dbt_model` should be `unique` and `not_null`
  - `id` in `my_second_dbt_model` should be `unique` and `not_null`
- Let's verify that by running those tests:
  - `dbt test -m my_first_dbt_model`
  - `dbt test -m my_second_dbt_model`
- In the BigQuery interface, in your personal dataset, go check that
  - `my_first_dbt_model` is a table
  - `my_second_dbt_model` is a view - this matches what you've written in the config of each of your models

Few tips 💡
- If you want to refresh all your models, or run all your tests, no need to specify the model with the `-m xxxx` parameter :
  - `dbt run` refreshes all your DBT models
  - `dbt test` runs all the tests configured in the project
- Remember the tests you implemented in SQL in Week 1 - Day 2 ? The concept of a test was "it fails if the SQL query returns at least 1 record". Go check the actual "compiled" tests that DBT has interpreted by going to `target/run/dbt_lewagon/models/example/schema.yml/` : this is where you'll find the tests that come directly from the setup done in the `schema.yml` file. If you open one of the unicity tests, like `unique_my_first_dbt_model_id.sql`, you'll see it has the classic structure :
  ```sql
  select
      unique_field,
      count(*) as n_records
  from dbt_test__target
  group by unique_field
  having count(*) > 1
  ```
