# Twitter API

Now that we have played a bit with Flask, it's time to start the exercises which will keep us busy for the rest of the day. The goal is to build a clone of the [Twitter API](https://developer.twitter.com/en/docs/api-reference-index) using Flask and different Flask plugins (like [these](https://github.com/humiaozuzu/awesome-flask)).

⚠️ In this exercise, we will implement some API endpoints with a relational database.

## Getting started

Let's start a new Flask project:

```bash
cd ~/code/<user.github_nickname>
mkdir twitter-api && cd twitter-api
pipenv --python 3.8
pipenv install flask
touch wsgi.py
```

### Factory Pattern

In the previous example, we initialized the `Flask` application right in the `wsgi.py`. Doing so, `app` was a global variable. The problem with this approach is it makes it harder to test in isolation. The solution to this problem is to use [Application Factories](http://flask.pocoo.org/docs/patterns/appfactories/), a pattern which will turn useful to make our app more modular (i.e. with multiple "small" files rather than some "big" ones).

👉 Take some time to read [this page of the Flask documentation](http://flask.pocoo.org/docs/patterns/appfactories/)

Let's use this approach:

```bash
mkdir app             # This is our main application's package.
touch app/__init__.py # And open this file in VS Code
```

```python
# app/__init__.py
# pylint: disable=missing-docstring

from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route('/hello')
    def hello():
        return "Hello World!"

    return app
```

Then open the `./wsgi.py` file and import this new `create_app` to use it right away:

```python
# ./wsgi.py

from app import create_app

application = create_app()
if __name__ == '__main__':
    application.run(debug=True)
```

Go ahead and launch the app:

```bash
FLASK_ENV=development pipenv run flask run
```

The server should start. Open your browser and visit [`localhost:5000/hello`](http://localhost:5000/hello). You should see "Hello world!" as a text answer!

### Namespace

The code in `app/__init__.py` is a copy/paste from the previous exercise, we just took the code and put it into a `create_app` method, returning the instance of `Flask` created. We can do better!

We will use the [`flask-restx`](https://flask-restx.readthedocs.io/) package:

```bash
pipenv install flask-restx
```

Take some time to read the following article:

:point_right: [Quick Start](https://flask-restx.readthedocs.io/en/stable/quickstart.html)

We want to start on the right foot in term of scalability, again take some time to read this:

:point_right: [Scaling your project](https://flask-restx.readthedocs.io/en/stable/scaling.html)

```bash
mkdir app/apis
touch app/apis/tweets.py
```

```python
# app/apis/tweets.py
# pylint: disable=missing-docstring

from flask_restx import Namespace, Resource

api = Namespace("tweets")


@api.route("/hello")
class TweetResource(Resource):
    def get(self):
        return "Hello from the 'tweets' namespace!"
```

:bulb: By using to our "tweets" namespace `api = Namespace("tweets")`, our "hello" API route will become `/tweets/hello` instead of just `/hello`

:bulb: The `get` method defined above will be called when the server receives an HTTP GET request on `/tweets/hello`

We can now import our simple namespace into our main application, like this:

```python
# app/__init.py__
# pylint: disable=missing-docstring

from flask import Flask
from flask_restx import Api

def create_app():
    app = Flask(__name__)

    from .apis.tweets import api as tweets
    api = Api()
    api.add_namespace(tweets)
    api.init_app(app)

    app.config['ERROR_404_HELP'] = False
    return app
```

If you stopped your server, restart it with:

```bash
FLASK_ENV=development pipenv run flask run
```

Open your browser and visit [`localhost:5000/tweets/hello`](http://localhost:5000/tweets/hello). You should see "Hello from the 'tweets' namespace!" as a text answer!

💡 It's important to understand the `from .apis.tweets import api as tweets` line which happens before the namespace registering. The `from .apis.tweets` means that we look into the `apis/tweets.py` file from the **same** package as the local `__init__.py`. It's a shortcut for `from app.apis.tweets`. Then the `import api` means that we import the variable or method `api` defined in this `tweets.py` file (here it's a variable: an instance of `Namespace`). The `as tweets` just renames the `api` that we imported to `tweets`, for readability.

### Testing

Let's set up our app so that writing test is easy and TDD is possible:

```bash
pipenv install flask-testing nose --dev
```

Let's create our `tests` folders and a first file

```bash
mkdir tests
mkdir tests/apis
touch tests/apis/__init__.py
touch tests/apis/test_tweet_views.py
```

```python
# tests/apis/test_tweet_view.py
from flask_testing import TestCase
from app import create_app

class TestTweetView(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        return app

    def test_tweet(self):
        response = self.client.get("/tweets/hello")
        text = response.data.decode()
        print(text)
        self.assertIn("Goodbye", text)
```

Open the terminal and run:

```bash
pipenv run nosetests -s tests/apis/test_tweet_view.py
```

The test should be red!

👉 How can you fix the test to make the command turn green?
👉 Do we need the `print()` statement in the test method? Why (not)?

### Deployment

We want to use Gunicorn and Heroku for production:

```bash
pipenv install gunicorn
echo "web: gunicorn wsgi --access-logfile=-" > Procfile
```

Finally let's set up git:

```bash
git init
git add .
git commit -m "New flask project boilerplate"
```

By that time, you should already have created 5 applications (which is the free limit).

So we need to `do to some cleaning`.
First we want to get application name in order to remove it :

```bash
heroku apps  # Display created apps
# === <your_mail> Apps
# <app_name_1> (eu)
# <app_name_2> (eu)
# <app_name_3> (eu)
# <app_name_4> (eu)
# <app_name_5> (eu)
```

Then we can remove it :

```bash
heroku apps:destroy <app_name_1>
# !    WARNING: This will delete <app_name_1> including all add-ons.
# !    To proceed, type <app_name_1> or re-run this command with
# !    --confirm <app_name_1>

<app_name_1>  # Type <app_name_1> and press <Enter>
# Destroying <app_name_1> (including all add-ons)... done
```

**Proceed to this operation each time needed.**

We can now create an app to be deployed on Heroku:

```bash
heroku create --region=eu
git push heroku master

heroku open # Check the app is actually running.
```

## First API endpoint - `/tweets/:id`

In the following section, we will implement the HTTP API serving a JSON of a single tweet.

### Basic Model

Before rushing to the Flask namespace we need to create to serve an HTTP response,
we need a model to hold some data and a database to persit this data through time.

Let's think about our `Tweet` and use TDD to implement this class. Have a look at
what [a Tweet is](https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/get-statuses-show-id#example-response) and you'll see that is quite complex.
Let's simplify by saying a tweet will hold some `text` and `created_at` date.

### TDD

Let's use TDD to implement this `Tweet` class with its two instance variables. We will write
the test first and then walk our way until the test turns green.

```bash
touch tests/test_models.py
```

```python
# tests/test_models.py
from unittest import TestCase
from app.models import Tweet  # We will code our `Tweet` class in `app/models.py`

class TestTweet(TestCase):
    def test_instance_variables(self):
        # Create an instance of the `Tweet` class with one argument
        tweet = Tweet("my first tweet")
        # Check that `text` holds the content of the tweet
        self.assertEqual(tweet.text, "my first tweet")
        # Check that when creating a new `Tweet` instance, its `created_at` date gets set
        self.assertIsNotNone(tweet.created_at)
        # Check that the tweet's id is not yet assigned when creating a Tweet in memory
        self.assertIsNone(tweet.id)
```

👉 Take some time to read the [26.4. `unittest`](https://docs.python.org/3/library/unittest.html) chapter.

OK, the test is written, let's run it! (it should not be green):

```bash
pipenv run nosetests tests/test_models.py
```

💡 _In the command above ☝️, we give the exact filename to run only this test file_

You should get something which looks like this:

```bash
======================================================================
1) ERROR: Failure: ModuleNotFoundError (No module named 'app.models')
----------------------------------------------------------------------
    # [...]
    tests/test_models.py line 2 in <module>
      from app.models import Tweet
   ModuleNotFoundError: No module named 'app.models'
```

:question: What's next? **Read the error message and try to fix it**

<details><summary markdown='span'>View solution
</summary>

You must create the `models.py` file so that this module is defined!

```bash
touch app/models.py
```

</details>

<br />

Run the tests again **until the error message changes**. You should get this one:

```bash
======================================================================
1) ERROR: Failure: ImportError (cannot import name 'Tweet')
----------------------------------------------------------------------
    # [...]
    tests/test_models.py line 2 in <module>
      from app.models import Tweet
   ImportError: cannot import name 'Tweet'
```

:question: What is the **minimum** code change you can do to fix this error?

<details><summary markdown='span'>View solution
</summary>

The error complains about the fact that `Tweet` is not defined. The minimum code
change we can do is to create an **empty** class:

```python
# app/models.py
class Tweet:
    pass
```

</details>

<br />

The next error should be:

```bash
======================================================================
1) ERROR: test_instance_variables (test_models.TestTweet)
----------------------------------------------------------------------
   Traceback (most recent call last):
    tests/test_models.py line 6 in test_instance_variables
      tweet = Tweet("my first tweet")
   TypeError: Tweet() takes no arguments
```

:question: What is the **minimum** code change you can do to fix this error?

<details><summary markdown='span'>View solution
</summary>

Our `Tweet` class is empty and needs an [instance variable](https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables) `text`:

```python
# app/models.py
# pylint: disable=missing-docstring

class Tweet:
    def __init__(self, text):
        self.text = text
```

</details>

<br />

The next two errors should complain about:

```bash
'Tweet' object has no attribute [...]
```

:question: How can we fix this last two errors and make the test pass?

<details><summary markdown='span'>View solution
</summary>

Our `Tweet` class is missing the `created_at` instance variable, automatically
set to [the current time](https://stackoverflow.com/questions/415511/how-to-get-current-time-in-python).
It's also missing the `id` instance variable, set to `None` on instance creation.

```python
# app/models.py
# pylint: disable=missing-docstring

from datetime import datetime

class Tweet:
    def __init__(self, text):
        self.id = None
        self.text = text
        self.created_at = datetime.now()
```

</details>

<br />

✨ Congrats! You just implemented the `Tweet` class using TDD.



## Setting up SQLAlchemy & Database

Like in the previous exercise, we need to install some tools:

```bash
pipenv install psycopg2-binary gunicorn
pipenv install flask-sqlalchemy flask-migrate flask-script
```

We will need to configure the used Database from an environment variable, the easiest is to use the `python-dotenv` package with a `.env` file:

```bash
touch .env
echo ".env" >> .gitignore
```

And add the `DATABASE_URL` variable:

```bash
# .env
DATABASE_URL="postgresql://postgres:<password_if_necessary>@localhost/twitter_api_flask"

# On OSX:
# DATABASE_URL="postgresql://localhost/twitter_api_flask"
```

If you got a `sqlalchemy.exc.OperationalError` verify your `DATABASE_URL`. Your password shouldn't contains `<`, `>` symbols.

```bash
# Valid example
DATABASE_URL="postgresql://postgres:root@localhost/twitter_api_flask"

# Invalid example
DATABASE_URL="postgresql://postgres:<root>@localhost/twitter_api_flask"
```

We now need to create a config object to pass to the Flask application. This will link the env variables to the actual Flask / SQLAlchemy configuration:

```bash
touch config.py
```

```python
import os

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
```

Now let's instantiate an `SQLAlchemy` instance which we will use for all SQL queries (CRUD).

```python
# app/__init__.py
# pylint: disable=missing-docstring

# [...]
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    from config import Config
    app.config.from_object(Config)
    db.init_app(app)

    # [...]
```

### Model

Now it's time to **convert** our existing `Tweet` model to a proper SQLAlchemy model, and not just a regular class. Open the `app/models.py` file and update it:

```python
# app/models.py
# pylint: disable=missing-docstring

from datetime import datetime

from app import db

class Tweet(db.Model):
    __tablename__ = "tweets"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(280))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Tweet #{self.id}>"
```

We can also get rid of the tests on the model as it's no longer a regular class. We trust SQLAlchemy with the column behavior, and as we have no instance method here, no need for unit testing:

```bash
rm tests/test_models.py
```

### Alembic setup

We need a local database for our application:

```bash
winpty psql -U postgres -c "CREATE DATABASE twitter_api_flask"

# MAC OS
# createdb twitter_api_flask
```


Then, we need to change the file `app/__init__.py` so that `flask-migrate` can identify the changes made in the Python app models in order to transcribe them as a migration in the db:



```python
# app/__init__.py
# [...]
from app.models import Tweet
from flask_migrate import Migrate

# After db.init_app(app)
migrate = Migrate(app, db)
# [...]
```

Now we can use Alembic (run `pipenv graph` to see where it stands)!

```bash
pipenv run flask db init

```

This command has created a `migrations` folder, with an empty `versions` in it. Time to run the first migration with the creation of the `tweets` table from the `app/models.py`'s `Tweet` class.

```bash
pipenv run flask db migrate -m "Create tweets table"
```

Open the `migrations/versions` folder: can you see a first migration file? Go ahead, open it and read it! That's a file you **can** modify if you are not happy with what has been automatically generated. Actually that's something the tool tells you:

```bash
# ### commands auto generated by Alembic - please adjust! ###
```

When you are happy with the migration, time to run it against the local database:

```bash
pipenv run flask db upgrade
```

And that's it! There is now a `tweets` table in the `twitter_api_flask` local database. It's empty for now, but it does exist!

## Adding a first tweet from a shell

We want to go the "manual testing route" to update the API controller code by adding manually a first Tweet in the database. It will validate that all our efforts to add SQLAlchemy are starting to pay off:

```bash
pipenv run flask shell
>>> from app import db
>>> from app.models import Tweet
>>> tweet = Tweet(text="Our first tweet!")
>>> db.session.add(tweet)
>>> db.session.commit()
# Did it work?
>>> db.session.query(Tweet).count()
>>> db.session.query(Tweet).all()
# Hooray!
```

### Controller + Route

It's now time to add a new route to our app to serve our API endpoint.
Remember, we want to have this:

```bash
GET /tweets/1

=> a JSON of the given tweet
```

Let's  do some TDD and implement our test before coding this new route.
Add the following code in `tests/apis/test_tweet_view.py`

```python
# tests/apis/test_tweet_view.py

from flask_testing import TestCase
from app import create_app, db  # N'oubliez pas d'importer db
from app.models import Tweet

class TestTweetViews(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = f"{app.config['SQLALCHEMY_DATABASE_URI']}"

    def test_tweet_show(self):
        first_tweet = Tweet(text="First tweet")
        db.session.add(first_tweet)
        db.session.commit()
        response = self.client.get("/tweets/1")
        response_tweet = response.json
        print(response_tweet)
        self.assertEqual(response_tweet["id"], 1)
        self.assertEqual(response_tweet["text"], "First tweet")
        self.assertIsNotNone(response_tweet["created_at"])
```

Do you see something wrong here if we keep the test like it is ?
Let's take a step back. What would happen if you execute this following code multiple times?

```python
tweet = Tweet(text="A test tweet")
db.session.add(tweet)
db.session.commit()
```

That's right! It would **create a record** on the database. Which means that if you run the tests 10 times, it will create 10 records! Way to pollute your development environment :disappointed_relieved:

The solution is to:

- Run the test against _another_ test database schema
- Clean up the schema (deleting all tables/recreating them) between every test run (every method even!)

Here is how we are going to achieve this goal. First we need to create a new database locally:

```bash
winpty psql -U postgres -c "CREATE DATABASE twitter_api_flask_test"

# MAC OS
# createdb twitter_api_flask_test
```

And then we can update our `TestTweetViews` class with:

```python
# tests/apis/test_tweet_views.py

from flask_testing import TestCase
from app import create_app, db  # Don't forget to take the db import
from app.models import Tweet

class TestTweetViews(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = f"{app.config['SQLALCHEMY_DATABASE_URI']}_test"
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # [...]
```


💡 If you run the test, you will get an error

```bash
pipenv run nosetests tests/apis/test_tweet_views.py
```



Now, let's make the test pass! You can remove the `/hello` route by replacing the content of this file entirely:

```python
# app/apis/tweets.py
# pylint: disable=missing-docstring

from flask_restx import Namespace, Resource, fields, abort
from app.models import Tweet
from app import db

api = Namespace('tweets')  # Base route

json_tweet = api.model('Tweet', {
    'id': fields.Integer(required=True),
    'text': fields.String(required=True, min_length=1),
    'author': fields.String(required=True, min_length=1),
    'created_at': fields.DateTime(required=True),
})

@api.route('/<int:id>')  # route extension (ie: /tweets/<int:id>)
@api.response(404, 'Tweet not found')
@api.param('id', 'The tweet unique identifier')
class TweetResource(Resource):
    def get(self, id):
        tweet = db.session.query(Tweet).get(id)
        if tweet is None:
            api.abort(404, "Tweet {} doesn't exist".format(id))
        else:
            return tweet

```
Take your time to read the code and make sure to understand it. As you can see, we have created a `json_tweet` object that we don't use yet in our code...

bulb: **Hint**: you need to use `@api.marshal_with` & `json_tweet` described [in the doc](https://flask-restx.readthedocs.io/en/stable/quickstart.html#data-formatting) to overcome the following error:

```bash
TypeError: Object of type Tweet is not JSON serializable
```

Do you understand this error? If not, ask your buddy then ask a TA!

```bash
pipenv run nosetests tests/apis/test_tweet_views.py
```

:bulb: **Hint**: have a look at the [full example](https://flask-restx.readthedocs.io/en/stable/example.html) from the documentation!

<details><summary markdown='span'>View solution (Really try first 🙏)
</summary>

We will use the Flask-RESTX built-in serialization:

```python
# app/apis/tweets.py
# pylint: disable=missing-docstring

from flask_restx import Namespace, Resource, fields, abort
from app.models import Tweet
from app import db

api = Namespace('tweets')

json_tweet = api.model('Tweet', {
    'id': fields.Integer,
    'text': fields.String,
    'created_at': fields.DateTime
})


@api.route('/<int:id>')
@api.response(404, 'Tweet not found')
@api.param('id', 'The tweet unique identifier')
class TweetResource(Resource):
    @api.marshal_with(json_tweet)
    def get(self, id):
        tweet = db.session.query(Tweet).get(id)
        if tweet is None:
            api.abort(404)
        else:
            return tweet
```

</details>


Good job! One Route done! Let's keep pushing.
## Setting up Github Actions

Setting up GitHub Actions for a project where you have a real PostgreSQL database is not as trivial as for a project without a database. Let's see how we can take the **configuration of GitHub Actions** already mentioned:

```bash
mkdir -p .github/workflows
touch .github/workflows/first-workflow.yml
```

```yml
# .github/workflows/first-workflow.yml
name: Build and Tests

on: push

jobs:
  build:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:latest
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: twitter_api_flask_test
        ports:
          - 5432:5432
        # needed because the postgres container does not provide a healthcheck
        options: --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.9
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: psycopg2 prerequisites
      run: sudo apt-get install libpq-dev
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pipenv
        pipenv install --dev
    - name: Test with nose
      run: |
        pipenv run nosetests
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost/twitter_api_flask
```

Version & push this change. Then go to your Github repository and check out the `Actions` tab. You should see a new "workflow run" there with the name of your commit. You can click on it and then on "Build" to see the build in real time.
After about 3 minutes, the tests should pass and the action should be validated. If not, open a ticket with a TA.

### Swagger documentation

The Flask-RESTx package comes with [swagger doc](https://flask-restx.readthedocs.io/en/stable/swagger.html) embeded. Run your server and access the root URL:

:point_right: [http://localhost:5000](http://localhost:5000)

Can you see the documentation? You can try your endpoints right within it!

### Going further

If you reached this part, you get the gist of building a RESTful API with Flask. It's time to practise!

- Implement the remaining endpoints to have a full `CRUD` RESTful API! Today we don't care about User Authorization for create, update & delete. [The doc is your friend](https://flask-restx.readthedocs.io/en/stable/)
- Use the GitHub flow for each new endpoint!
- Deploy often! Everytime you merge a branch with a new endpoint, `git push heroku master`!

Good luck 😉


----

----

:question: Implement the rest of `app/apis/tweets.py` to make the test pass.

Here are the test you need to pass to implement the other routes:

```python

# ....
 def test_tweet_show(self):
        first_tweet = Tweet(text="First tweet")
        db.session.add(first_tweet)
        db.session.commit()
        response = self.client.get("/tweets/1")
        response_tweet = response.json
        print(response_tweet)
        self.assertEqual(response_tweet["id"], 1)
        self.assertEqual(response_tweet["text"], "First tweet")
        self.assertIsNotNone(response_tweet["created_at"])

    def test_tweet_create(self):
        response = self.client.post("/tweets", json={'text': 'New tweet!'})
        created_tweet = response.json
        self.assertEqual(response.status_code, 201)
        self.assertEqual(created_tweet["id"], 1)
        self.assertEqual(created_tweet["text"], "New tweet!")

    def test_tweet_update(self):
        first_tweet = Tweet(text="First tweet")
        db.session.add(first_tweet)
        db.session.commit()
        response = self.client.patch("/tweets/1", json={'text': 'New text'})
        updated_tweet = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_tweet["id"], 1)
        self.assertEqual(updated_tweet["text"], "New text")

    def test_tweet_delete(self):
        first_tweet = Tweet(text="First tweet")
        db.session.add(first_tweet)
        db.session.commit()
        self.client.delete("/tweets/1")
        self.assertIsNone(db.session.query(Tweet).get(1))

```

To check if you are making some progress, run the tests:

```bash
nosetests
```

<details><summary markdown='span'>View solution (Really try first 🙏)
</summary>

```python
from flask_restx import Namespace, Resource, fields
from app.models import Tweet
from app import db

api = Namespace('tweets')  # Base route

json_tweet = api.model('Tweet', {
    'id': fields.Integer(required=True),
    'text': fields.String(required=True, min_length=1),
    'created_at': fields.DateTime(required=True),
})

json_new_tweet = api.model('New tweet', {
    'text': fields.String(required=True, min_length=1),  # Don't allow empty string
})

@api.route('/<int:id>')  # route extension (ie: /tweets/<int:id>)
@api.response(404, 'Tweet not found')
@api.param('id', 'The tweet unique identifier')
class TweetResource(Resource):
    @api.marshal_with(json_tweet)
    def get(self, id):
        tweet = db.session.query(Tweet).get(id)
        if tweet is None:
            api.abort(404, "Tweet {} doesn't exist".format(id))
        else:
            return tweet

    @api.marshal_with(json_tweet, code=200)
    @api.expect(json_new_tweet, validate=True)
    def patch(self, id):
        tweet = db.session.query(Tweet).get(id)
        if tweet is None:
            api.abort(404, "Tweet {} doesn't exist".format(id))
        else:
            tweet.text = api.payload["text"]
            db.session.commit()
            return tweet

    def delete(self, id):
        tweet = db.session.query(Tweet).get(id)
        if tweet is None:
            api.abort(404, "Tweet {} doesn't exist".format(id))
        else:
            db.session.delete(tweet)
            db.session.commit()
            return None


@api.route('')
@api.response(422, 'Invalid tweet')
class TweetsResource(Resource):
    @api.marshal_with(json_tweet, code=201)
    @api.expect(json_new_tweet, validate=True)
    def post(self):
        text = api.payload["text"]
        if len(text) > 0:
            tweet = Tweet(text=text)
            db.session.add(tweet)
            db.session.commit()
            return tweet, 201
        else:
            return abort(422, "Tweet text can't be empty")

    @api.marshal_with(json_tweet)
    def get(self):
        return db.session.query(Tweet).all(), 201

```

</details>


## I'm done

Before you jump to the next exercise, let's mark your progress with the following:

```bash
cd ~/code/<user.github_nickname>/reboot-python
cd 03-Back-end/03-Twitter-API
touch DONE.md
git add DONE.md && git commit -m "03-Back-end/03-Twitter-API done"
git push origin master
```
