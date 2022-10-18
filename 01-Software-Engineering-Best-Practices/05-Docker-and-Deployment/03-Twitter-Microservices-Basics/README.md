# 03 - Twitter Microservices Basics

Welcome!

In this challenge, you are provided with an extremely simplistic example of a Twitter microservice app with two services:

- A **Tweet** back-end service to interact with our tweets
- A new **User** service that interact with the Tweet Service
  - in this service, we can create **users**, list them all, and inspect the tweets they sent

These two services contained both a mimic of a database as a json file located in the folder `database`

🎯 Your goal is to :

- Recode the user service properly so that we get a sqlite database storing our users
- Implement a new endpoint `Timeline` to the user service in order to output the top 10 most recent tweets for every users.
- We will then set up the two services and ship them in containers in the next exercise

Ready? Let's go!

## Understand the code


First, let's navigate to the right folder

```bash
cd ~/code/<user.github_nickname>/04-Microservices-and-Containers/03-Twitter-Microservices-Basics
pipenv install --dev 
code .
```

Let's start and consume the two services before diving into the code.

```bash

pipenv run python services/tweet.py

```

Now head over to <http://localhost:5000/> and try the tweet service!
As you can see, this service only contains one endpoint to list all tweets.
The database contained some tweets already stored in a json file.

Let's inspect now the user service.
Don't close your web server.

Open a new terminal and execute the following command :

```bash

pipenv run python services/user.py

```

Now head over to <http://localhost:5001/> and play with the user services.
Have you seen the `users/<username>/tweets` endpoint?
Try it with this for the user `brian_smith` : <http://localhost:5001/users/brian_smith/tweets>

How did we reach the tweet service? Well, it's nothing more then an API call to the tweet service!
Please, inspect the file `services/user.py` to understand the full code!

## Let's properly code our microservices Twitter app

To do so, we will recode our two services with a proper SQLite database.

As you can see, we have already filled the `tweets` folder which contains the Twitter service with a proper SQLite DB.
Please inspect the files inside the `tweets` folder.
Do you see something different?
Look at the `model.py`...
Yes! A tweet now has a `user` attached to it!
Look at the `routes.py`...
Yes, we now have our day 3 REST API with the 4 CRUD operations implemented!

Your task is to recode the user service properly.

Ready? Let's go!
## Turn user into a microservice

Let's create a folder `users`

```bash
mkdir users
```

```bash
cd users
```

Let's set up our `Pipenv` and add some packages we will use

```
pipenv --python 3.8
pipenv install flask flask-migrate flask-sqlalchemy werkzeug==2.1.2 requests
```

Let's create our DB :

```bash
touch user.db
```

Let's add a model to represent our users:

```bash
touch models.py
```

```python
#models.py

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_app(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)

    def __repr__(self):
        return f'<user {self.id}, {self.username}>'

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
        }
```

Let's add our different endpoints in a `routes.py``

```bash
touch routes.py
```

```python
#routes.py
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import NotFound, ServiceUnavailable
import requests
from models import db, User


user_blueprint = Blueprint('user_api_routes', __name__,
                           url_prefix='/users')


@user_blueprint.route('', methods=['GET'])
def test():
    return jsonify({
        "url": "/",
        "subresource_urls": {
            "all_users": "/users/all",
            "user_info": "/users/<username>",
            "user_all_tweets": "/users/<username>/tweets",
            "user_timeline": "/users/<username>/suggested"
        }
    })


@user_blueprint.route('/all', methods=['GET'])
def get_all_users():
    all_user = User.query.all()
    result = [user.serialize() for user in all_user]
    response = {
        'message': 'Returning all users',
        'result': result
    }
    return jsonify(response)


@user_blueprint.route('/create', methods=['POST'])
def create_user():
    try:
        user = User()
        user.username = request.form["username"]
        db.session.add(user)
        db.session.commit()

        response = {'message': 'User Created', 'result': user.serialize()}
    except Exception as e:
        print(str(e))
        response = {'message': 'Error in creating response'}
    return jsonify(response)



@user_blueprint.route('/<username>/exists', methods=['GET'])
def user_exists(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"result": True}), 200

    return jsonify({"result": False}), 404


@user_blueprint.route("<username>/tweets", methods=['GET'])
def user_tweets(username):
    """
    Gets all tweets  from the 'tweets Service' for one specific user
    :return: List of all the user's tweets
    """
    user = User.query.filter_by(username=username).first()
    if not user:
        raise NotFound("User '{}' not found.".format(username))
    print(user)
    try:
        users_tweets = requests.get("http://127.0.0.1:9000/tweets")
    except requests.exceptions.ConnectionError:
        raise ServiceUnavailable("The tweets service is unavailable.")

    if users_tweets.status_code == 404:
        raise NotFound("No tweets were found for {}".format(username))
    tweets = users_tweets.json()
    print(tweets)
    tweets = ([tweet["text"] for tweet in tweets if username == tweet["username"]])
    return jsonify(tweets)


@user_blueprint.route("<username>/tweet_shows", methods=['GET'])
def user_recommendation(username):
    """
    Gets Twitter timeline information from the 'tweets Service' for the user, and
     movie ratings etc., from the 'Movie Service' and returns a list.
    :param username:
    :return: List of Users tweets
    """
    return "You need to fill this part!"
```

Let's now instantiate our flask app.

```bash
touch wsgi.py
```

```python
#in wsgi.py
from flask import Flask

from flask_migrate import Migrate
import models
from routes import user_blueprint


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
    models.init_app(app)
    app.register_blueprint(user_blueprint)

    migrate = Migrate(app, models.db)
    return app

application = create_app()
if __name__ == '__main__':
    application.run()
```

Great! Let's now start the newly updated tweet service. You can close the previous web servers running and open a new terminal :

```bash
cd ../tweets
```

Let's install the packages we need to run the service.

```bash
pipenv install
```

Let's start the web server and try our tweet service.

```bash
FLASK_ENV=development pipenv run flask run
```

Now head over to <http://localhost:5000/>.
Great, you should see all our CRUD endpoints working fine and some tweets already in the database! How so? Well, as you can see, there is already a `migration` folder with some migrations runned on the `tweet.db` ;)
Good job.

Let's now try and check out our users services.
Open a new terminal and run the following command:

```bash
cd ../users
```

Let's initialize our database.

```bash
pipenv run flask db init
```


```bash
pipenv run flask db migrate
```

And now, we can launch our user service :

```bash
FLASK_ENV=development pipenv run flask run --port 5001
```

Now head over to <http://localhost:5000/users>.

Cool, everything works fine he?
What happens if you go to <http://localhost:5000/users/all> ?
Error message! Well, it's normal, you don't have any users in your database yet!

Let's add two users :

- user with username `laura_jane`
- user with username `oliver_smith`

Add some users in your database with the `users/create` endpoint
You can use [Postman](<https://www.postman.com/>) to make it easy testing your request.
You can install [Postman Agent](<https://www.postman.com/downloads/postman-agent/>) to be able to test a POST request locally on your machine.
When doing your request on Postman, please click select POST, then Body, then form-data as described in the image to send this parameter to the API.

<center>
<img src="https://github.com/lewagon/fullstack-images/blob/master/reboot-python/postman_query.png?raw=true" />
</center>

Good job!
Your job now is to implement the `<username>/tweet_shows`endpoints and to fill the
method `user_recommendation`.
The goal of this endpoint is to recommend to any user the ten most recent tweets in the database that the user did **not** write. You can use the user `laura_jane` to test your code.

To do so, you would need first to :

- 1. retrieve the user with its username and check that he exists in the DB
- 2. retrieve all the tweets from the service tweet by calling the service
- 3. filter these tweets to keep the 10 most recent tweets which the user did not write

Hint :

- You can have a [look](https://docs.sqlalchemy.org/en/14/orm/query.html) at the documentation from SQL Alchemy and use the `query.filter_by` method for the step 1.

Done? Good job! Here is your first glimpse of a microservice app
In the next exercise, we will see how to deploy this multi-services app with docker-compose and how to improve it even more.
