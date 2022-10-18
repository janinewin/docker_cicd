from flask import Flask, jsonify
import json
import os
from werkzeug.exceptions import NotFound

app = Flask(__name__)



root_dir = os.path.dirname(os.path.realpath(__file__ + '/..'))

with open("{}/database/tweets.json".format(root_dir), "r") as f:
    tweets = json.load(f)

@app.route("/", methods=['GET'])
def hello():
    return jsonify({
        "uri": "/",
        "subresource_uris": {
            "tweets": "/tweets",
            "tweet": "/tweets/<username>"
        }
    })


@app.route("/tweets", methods=['GET'])
def tweet_list():
    return jsonify(tweets)


@app.route("/tweets/<username>", methods=['GET'])
def tweet_record(username):
    if username not in tweets:
        raise NotFound

    return jsonify(tweets[username])

if __name__ == "__main__":
    app.run(port=5000, debug=True)

