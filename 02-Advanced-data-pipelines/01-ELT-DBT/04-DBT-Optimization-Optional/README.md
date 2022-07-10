## High level goal

_Note : there's no action item in this section_

There are 3 main issues in the previous setups we've done, that are not optimal
1. When picking data from the last 20 days of the Hackernews dataset, we've harcoded in the code the value `20` : this should never be the case. This variable should be centralized somewhere
2. When we were counting the `num_comments`, `num_stories`, the first and the last time those comments or stories were written : we were writing a lot of duplicated code.
3. The loading of some of the models is very heavy everytime we run the script : we should find a way to make this load lighter
4. If we were to document the project more, we would be defining the same fields multiple times, in different places. We should centralize this documentation.

## Instructions

_First : copy `dbt_lewagon` from the previous challenge section into this one_

### Create variables

- In the `dbt_project.yml`, introduce a variable called `last_x_days_history`, that you'll set to `20`. And use that variable when building the `stg_hackernews_full.sql` model. Search the DBT documentation yourself to understand how things should be setup.
  Correction is in the `stg_hackernews_full_1.sql` and `dbt_project.yml` files
- Run `make test` - `test_dbt_project_created` and `test_dbt_variable_created` should succeed.
- Push to git.


### Don't Repeat Yourself - Macros

- In the `mart_user` model, we were reusing some code a lot. In order to avoid that, write 3 macros (those macros should be written in a file you would create here : `dbt_lewagon/macros/models/mart_user.sql`) :
  - 1 called `num_types` : which takes a given type as an argument. Counts the distinct number of occurences of that type in the aggregation. And also returns the name of the column associated to this calculation.
  - 1 called `first_type_at` : which takes a given type as an argument. And returns when that type happened the first time (based on `created_at_local`) for a given level of aggregation. It also returns the name of the column associated to this calculation
  - 1 called `last_type_at` : same as above, but for the most recent occurence of the type
- To be more precise :
  - `{{ num_types('comment') }}` should output a piece of code like that : `COUNT(xxxxx) AS num_comment` (let's simplify and keep column names singular - this will change a bit from the previous name you gave to that column)
  - `{{ first_type_at('comment') }}` should output a piece of code like that : `OPERATION(xxxxx) AS first_comment_at` etc
  - If you need help on this, you can read this documentation : [Jinja](https://docs.getdbt.com/docs/building-a-dbt-project/jinja-macros)

The correction is in 2 files :
- `mart_user_macro_1.sql` is the expected macro
- `mart_user_model_1.sql` is the `mart_user` model, modified to use the macro defined above

Your previous `mart_user` model should be calling macros 6 times total (3 macros per type. On 2 types).

- Build a macro called `key_metrics_per_type` which, for a given type, builds the 3 key metrics :
  - num_xxx
  - first_xxx_at
  - last_xxx_at ?
    Modify your `mart_user` to use this macro. It should now be calling it 2 times. 1 for each type.
- The correction is in 2 files :
  - `mart_user_macro_2.sql` is the expected macro
  - `mart_user_model_2.sql` is the expected `mart_user` model, modified to use the macro defined above.
- As a next step, you could make the code even more succinct by writing a FOR loop that iterates over a list that gathers the different types - but there's very little value in this : for the sake of optimization, we would be sacrificing the readibility of the query.


### Incremental models

Everytime you run the `stg_hackernews_full` model, it loads the entire dataset (it does not because we've limited to the last 10 days - but in reality, on the production environment, it would). Hence you would be processing 12GB everytime you run this script. Still, even on our dev environment, where we've limited the amount of data to be loaded, it's still loading 10 full days while the data of those previous days was already in the table.
- Make the `stg_hackernews_full` model an incremental model, which loads only the records that have not been inserted in the previous run. We won't give any indication on this - you should explore the DBT documentation by yourself. Run the model : `dbt run -m stg_hackernews_full` : do you notice how many records were inserted ?

The correction is in the file: `stg_hackernews_full_2.sql`
