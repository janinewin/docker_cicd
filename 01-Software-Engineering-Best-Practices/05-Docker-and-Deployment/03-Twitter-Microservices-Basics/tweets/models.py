# app/models.py
# pylint: disable=missing-docstring

from datetime import datetime

from tweets import db


class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(280))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(255))

    def __repr__(self):
        return f"<Tweet #{self.id}>"
