# ./wsgi.py
# app/__init__.py
# pylint: disable=missing-docstring

from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'vZK7siKrV8BL46KsyAIPoQ'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tweet.db'
    db.init_app(app)

    from models import Tweet
    from flask_migrate import Migrate

    # After db.init_app(app)
    migrate = Migrate(app, db)

    from routes import api as tweets
    api = Api()
    api.add_namespace(tweets)
    api.init_app(app)

    app.config['ERROR_404_HELP'] = False

    return app


application = create_app()
if __name__ == '__main__':
    application.run()
