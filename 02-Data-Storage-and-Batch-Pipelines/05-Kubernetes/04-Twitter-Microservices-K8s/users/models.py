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

