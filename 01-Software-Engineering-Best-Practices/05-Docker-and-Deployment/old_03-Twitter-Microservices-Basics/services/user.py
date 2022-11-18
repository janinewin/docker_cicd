from werkzeug.exceptions import NotFound, ServiceUnavailable
import json
from flask import Flask, jsonify
import os
import requests

app = Flask(__name__)

root_dir = os.path.dirname(os.path.realpath(__file__ + '/..'))
with open("{}/database/users.json".format(root_dir), "r") as f:
    users = json.load(f)


@app.route("/", methods=['GET'])
def hello():
    return jsonify({
        "url": "/",
        "subresource_urls": {
            "users": "/users",
            "user": "/users/<username>",
            "tweets": "/users/<username>/tweets",
            "timeline": "/users/<username>/suggested"
        }
    })

@app.route("/users", methods=['GET'])
def users_list():
    return jsonify(users)


@app.route("/users/<username>", methods=['GET'])
def user_record(username):
    if username not in users:
        raise NotFound
    return jsonify(users[username])


@app.route("/users/<username>/tweets", methods=['GET'])
def user_tweets(username):
    """
    Gets all tweets posted by user from the'Tweets Service', returns a list.
    :param username:
    :return: List of Users tweets
    """
    if username not in users:
        raise NotFound("User '{}' not found.".format(username))

    try:
        users_tweets = requests.get("http://127.0.0.1:5000/tweets/{}".format(username))
    except requests.exceptions.ConnectionError:
        raise ServiceUnavailable("The tweets service is unavailable.")

    if users_tweets.status_code == 404:
        raise NotFound("No tweets were found for {}".format(username))

    users_tweets = users_tweets.json()
    print(user_tweets)

    # Return all tweets posted by user
    return jsonify(users_tweets)


@app.route("/users/<username>/timeline", methods=['GET'])
def user_timeline(username):
    """
    TO DO: implement tweets timeline.
    The method should return a recommandation of tweets for one specific user.
    It should be a list containing the 10 most recent tweets written by users, excluding the current user's tweet
    :param username:
    :return: Suggested 10 tweets
    """
    pass


if __name__ == "__main__":
    app.run(port=5001, debug=True)
