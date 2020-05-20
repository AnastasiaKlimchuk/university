from datetime import datetime as dt

from core import db
from .base import Model


class Movie(Model, db.Model):
    __tablename__ = 'all_movies'

    # id -> integer, primary key
    id = db.Column(db.Integer, primary_key=True)
    # name -> string, size 50, unique, not nullable
    name = db.Column(db.String(50), nullable=False)
    # year -> integer
    year = db.Column(db.String(20))
    # genre -> string, size 20
    genre = db.Column(db.String(20))

    user_id = db.Column(db.Integer)

    def __init__(self, name, year, genre, user_id):
        self.name = name
        self.email = year
        self.genre = genre
        self.user_id = user_id

    def __repr__(self):
        return '<Movie {}>'.format(self.name)