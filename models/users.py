from core import db


class Data(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone
