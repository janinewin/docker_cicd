from flask import Blueprint, jsonify, request
from werkzeug.exceptions import NotFound, ServiceUnavailable
import requests
from models import db, User


user_blueprint = Blueprint('user_api_routes', __name__,
                           url_prefix='/user')


@user_blueprint.route('', methods=['GET'])
def test():
    return "welcome to our user page"


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
    Gets booking information from the 'tweets Service' for the user, and
     movie ratings etc. from the 'Movie Service' and returns a list.
    :param username:
    :return: List of Users tweets
    """
    user = User.query.filter_by(username=username).first()
    if not user:
        raise NotFound("User '{}' not found.".format(username))
    print(user)
    try:
        # users_tweets = requests.get(
        #     "http://127.0.0.1:9000/tweets/{}".format(username))
        users_tweets = requests.get("http://tweet-service:5002/tweets")
    except requests.exceptions.ConnectionError:
        raise ServiceUnavailable("The tweets service is unavailable.")

    if users_tweets.status_code == 404:
        raise NotFound("No tweets were found for {}".format(username))
    tweets = users_tweets.json()
    print(tweets)
    tweets = ([tweet["text"] for tweet in tweets if username == tweet["username"]])
    # For each booking, get the rating and the movie title
    return jsonify(tweets)


@user_blueprint.route("<username>/tweet_shows", methods=['GET'])
def user_recommendation(username):
    """
    Gets Twitter timeline information from the 'tweets Service' for the user, and
     movie ratings etc. from the 'Movie Service' and returns a list.
    :param username:
    :return: List of Users tweets
    """
    user = User.query.filter_by(username=username).first()
    if not user:
        raise NotFound("User '{}' not found.".format(username))
    print(user)
    try:
        # users_tweets = requests.get(
        #     "http://127.0.0.1:9000/tweets/{}".format(username))
        users_tweets = requests.get("http://tweet-service:5000/tweets")
    except requests.exceptions.ConnectionError:
        raise ServiceUnavailable("The tweets service is unavailable.")

    if users_tweets.status_code == 404:
        raise NotFound("No tweets were found for {}".format(username))
    tweets = users_tweets.json()
    print(tweets)
    tweets = ([tweet
              for tweet in tweets if username != tweet["username"]])

    top_ten_tweets = sorted(tweets, key=lambda d: d['created_at'], reverse=True)
    # For each booking, get the rating and the movie title
    return jsonify(top_ten_tweets)
