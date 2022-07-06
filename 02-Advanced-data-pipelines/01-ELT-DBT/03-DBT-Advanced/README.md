## High level goal

You've created your first staging models, which are refined versions of the `source` data inherited from the BigQuery dataset. This section has 2 goals :
- Building on top of those models (creating some models that are useful to the business)
- Making your code scalable : removing hard coded values from the code + building macros to avoid repetitive logic in your project

Once we have this whole setup in place, we'll make our environement cleaner by
- documenting our models
- writing some tests that should be executed against the columns

## Instructions

### Enrich the mart layer

- Under the `models/mart/` folder, create a file called `mart_user.sql`. You can execute the following command from `dbt_lewagon` : `touch models/mart/mart_user.sql`. It will log key information about the Hackernews users.
- Configure the model this way :
  - It should be a `view` materialization
  - It should be based on `stg_hackernews_full` model
  - It should be composed of this list of fields:
    - `user_id`
    - `num_comments` : the total number of comments made by the author
    - `first_comment_at` : when the user made his first comment on HackerNews
    - `last_comment_at` :  when the user made his last comment on HackerNews
    - `num_stories` :  the total number of stories made by the author
    - `first_story_at` :  when the user made his first story on HackerNews
    - `last_story_at` : when the user made his last story on HackerNews
- Run this model : `dbt run -m mart_user`
- **Suggested approach : do not try to write SQL for all the fields at once. Start with one very simple config, outputting 1 or 2 fields. Then run your model. And make sure it's created in BigQuery. Work very iteratively**

Now we want to be able to make sure that our way of calculating the `num_stories`, `num_comments` made by a user in the last 10 days is correct. This is called **QA**. To do that, you need, for a given `user_id`, to go check on the HackerNews' website if the volume of activites observed there matched the values in your `mart_user` model.
- To facilitate this, let's add a new field to the `mart_user` model : `user_url` which brings you to the welcome page of the user, where you can see the history of stories or comments they posted. This URL is a concatenation of `https://news.ycombinator.com/user?id=` and the `id` of the user. Run the model again : `dbt run -m mart_user`
- Now that you have this field handy, it should facilitate your QA : pick a few `user_id` in your BigQuery model, and verify that the `num_comments` or `num_stories` you calculated for this user matches the  `num_comments` and `num_stories` you observe on the HackerNews website, for this user URL.


### Document your models and add some tests

You've built a few models already - some folks in your company may need to use your models, to get some insights about the data. Thus, you should document what each field means. DBT has a standard way of documenting models - and this documentation can then be parsed and surfaced on a web page, accessible by everyone in the company.

- Under the  `models/mart/` folder, create a file called `models.yml`. `touch models/mart/models.yml`. Following the instructions on how to properly document a model : [Documentation](https://docs.getdbt.com/docs/building-a-dbt-project/documentation), document the `mart_user` model. For each of them :
  - Provide a high level `description` of the model itself
  - Provide a high level `description` of all the columns
- Implement 3 tests
  - 1 that checks that `user_id` is unique and always populated
  - 1 that checks that `num_comments` is always greater or equal to 0
  - 1 that checks that `num_stories` is always greater or equal to 0

_Hint : for the "always greater or equal to 0", check on the internet : you will need to install a DBT package that enables you to very simply configure this type of test : [dbt_utils](https://hub.getdbt.com/dbt-labs/dbt_utils/0.1.7/). You'll need to create a `packages.yml` file at the same level as the `dbt_project.yml` file, populate it, and then run `dbt deps` to install the package_

## Run the tests

- Let's make sure all the tests you've written are green. Run `dbt test`
- If tests are failing, go check the compiled SQL file referenced in the error message - you can copy paste the SQL code and execute it in BigQuery to better understand what the failing records are, and why the test is failing.


## Surface the documentation

You now have a robust DBT project : models that are dependent on each other. Documentation on the meaning of each field. Listing some tests etc. Let's surface all this documentation somewhere.

You can find most of commands we'll run here : [Documentation](https://docs.getdbt.com/reference/commands/cmd-docs). With some additional interesting information.

Run the following command :

- `dbt docs generate`
- Then `dbt docs serve`

### Fields documentation

This will open a page in your browser. Navigate through the documentation. Check the "Database" section, to find the structure of your BigQuery projects, the datasets below them, the tables / views they're made of, as well as the documentation of each field. Especially, go to
- Database > your project name > your dataset name > `mart_user` : you should be able to see the documentation you've written about the fields + the tests you put in place


### Lineage graph

Click on `stg_hackernews_full` (which you have not documented). At the bottom right of the screen click on the little blue logo, called `View Lineage Graph`. You can now see how your model is related to other models.