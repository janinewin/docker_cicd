# Introduction

There are 4 steps in this setup
1. Install DBT
2. Setup the connection configuration in order for DBT to be able to interact with BigQuery (write and read). This is done by creating a profile, filling a file called `profiles.yml`
3. Build a DBT project, which means
  2.1 Create the folder structure of your DBT project
  2.2 Fill the properties / information about this project in a config file called `dbt_project.yml`

# Setup the environment

## Install DBT

- Install DBT by downloading it on your local : follow the instructions [here](https://docs.getdbt.com/dbt-cli/install/pip) : IMPORTANT NOTE : the adapter in our case is `bigquery`. Hence the command you should execute is : `pip install dbt-bigquery`
- Make sure DBT is indeed installed by executing `dbt --version` in your terminal.

## Setup your profile

_High level info (no action item) : in this section, you'll have to setup a DBT profile - meaning populating a file called `profiles.yml`. 1 DBT project maps to 1 DBT profile, which generally maps to 1 company. Typically as a Le Wagon teacher, in my `profiles.yml` I have 2 profiles : 1 for LeWagon, 1 for the company I work at._

_Notes / Links_ : Official documentation to DBT profiles - and more specifically, profiles to connect to BigQuery
- [`profiles.yml`](https://docs.getdbt.com/reference/profiles.yml)
- [BigQuery profile](https://docs.getdbt.com/reference/warehouse-profiles/bigquery-profile)

- Your DBT profile should be stored in a folder at your root called `.dbt`. Open it or create  it by running : `code ~/.dbt/profiles.yml`. The documentation on how to setup this profile is here :
  - [`profiles.yml`](https://docs.getdbt.com/reference/profiles.yml)
  - More specifically, for a
- Call your profile `lewagon`
- This profile can write to multiple targets (targets means "**where** DBT creates tables and insert data). In our case, there'll be
  - a default target (your dev projects in BigQuery)
  - a production target (your prod projects in BigQuery)
  - and by default, we'll make this profile write to the default target.
- Hence : set the target to `default`
- In the `outputs` section:
  - create the `default` target
    - Make the `type` : `bigquery`
    - The method (connection method) : `service-account`
    - Keyfile (where is the key of this service account located) : in the previous section, you stored it in `~/.bigquery_keys/student-dev-service-account.json` : instead of the relative path, you need to give the absolute path though.
    - `project` (where this profile will write): `lewagon-dev-stg`
    - `dataset` (in which dataset it will write) : `dbt_the_first_letter_of_first_name+full_name` (if your name is Barack Obama, it should be `dbt_bobama`)
    - `location` (where your dataset will be hosted) : `US` ?
      - Why the `US` instead of `EU` ? Because the Hackernews public dataset is located in the US, it makes the connections work better.
    - `threads: 1`
    - `timeout_seconds: 300`
    - `priority: interactive`
    - `retries: 1`
  - create the `prod` target. Which as the exact same parameters as the default target. Except that :
    - `project` should be `lewagon-prod-stg`
    - `dataset` should be `prod`

Two things :
- Watch out with the levels of indendation in your `profiles.yml` file
- If you're struggling too much, download the solution of what your file should look like - but remember to adapt some of the parameters to your specific use case.

## Build the DBT project

- In your terminal, go to the `data-engineering-solutions/02-Advanced-data-pipelines/01-ELT-DBT` path. This is where we'll create the DBT project, that we will call `dbt_lewagon`
- Once there, you need to init (create the folder structure) of the DBT project - we'll call it `dbt_lewagon`.
  - In command lines, run `dbt init`. When prompted:
    - _Enter a name for your project (letters, digits, underscore)_ Enter: `dbt_lewagon`
    - _Which database would you like to use? Enter : 1 for <bigQuery>._ Enter: `1`
    - _Desired authentication method option (enter a number):_ Enter: `2`
    - _keyfile (/path/to/bigquery/keyfile.json):_ : Enter the absolute path of where you stored your BigQuery service account key, including the file name and its extension. Meaning it should look something like this :  `/Users/nicolasbancel/.gcp_keys/lewagon-nicolas-key.json` (If you spell it wrong, you'll be able to modify it later)
    - _project (GCP project id)_ : Self explanatory : Enter your company's GCP project ID
    - _dataset (the name of your dbt dataset)_ : Please be cautious here. Call it `dbt_{firstletteroffirstname}{last_name}_day1` hence if your name is Barack Obama, your dataset should be `dbt_bobama_day1`.
    - _threads (1 or more)_ : Enter `1`
    - _job_execution_timeout_seconds [300]_ : Enter `300`
    - _Desired location option (enter a number):_ : Enter `1` for `US`. This is important : the dataset we'll be exploring is located in the US - it facilitates things if you set up a "receiving" dataset that's also in the US.

This should have done 2 things
- It generated all the tree structure needed for the DBT project under the `dbt_lewagon` folder
- It should have created a `profiles.yml` file at the following location : `~/.dbt/profiles.yml`

## Verify the setup of `profiles.yml`

Let's check that the `profiles.yml` file is configured correctly :
- Your DBT profile should be stored in a folder at your root called `.dbt`. Open it by running : `code ~/.dbt/profiles.yml`. You should be able to see all the configuration you've set when creating the DBT project.
- Run your tests to make sure the setup is correct
  - outputs
  - name of profile
  - location
  - service account

## Verify the structure of the DBT project and enhance it

### `project.yml` file

_No action item in this section - we're just providing context. There's an action item if your setup does not match what's mentionned below_

- Open the `dbt_lewagon` folder, and open the `project.yml` file in this folder:
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

### Initial tree structure of the DBT project

_No action item in this section - we're just providing context. There's an action item if your setup does not match what's mentionned below_

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

### Enhance DBT project tree

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
```
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
├── dbt_packages
├── dbt_project.yml
├── logs
│   └── dbt.log
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
├── target
│   ├── compiled
│   ├── graph.gpickle
│   ├── manifest.json
│   ├── partial_parse.msgpack
│   ├── run
│   └── run_results.json
└── tests
```

## Run your first models and tests

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
- In the BigQuery interface, in your dataset, go check that
  - `my_first_dbt_model` is a table
  - `my_second_dbt_model` is a view
- Let's verify that by running those tests:
  - `dbt test -m my_first_dbt_model`
  - `dbt test -m my_second_dbt_model`
- If you want to refresh all your models, or run all your tests, no need to specify the model with the `-m xxxx` parameter :
  - `dbt run` refreshes all your DBT models
  - `dbt test` runs all the tests configured in the project
