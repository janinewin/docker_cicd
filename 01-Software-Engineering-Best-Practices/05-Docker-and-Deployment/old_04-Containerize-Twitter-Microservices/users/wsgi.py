from flask import Flask

from flask_migrate import Migrate
import models
from routes import user_blueprint


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'vZK7siKrV8BL46KsyAIPoQ'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
    models.init_app(app)
    app.register_blueprint(user_blueprint)

    migrate = Migrate(app, models.db)
    return app

application = create_app()
if __name__ == '__main__':
    application.run()
