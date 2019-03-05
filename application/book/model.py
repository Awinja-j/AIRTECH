from datetime import datetime
from manage import app, db


# class Book(db.Model):
#     pass

class Ticket(db.Model):
    __tablename__ = "ticket"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    date_created = db.Column(db.Integer, primary_key=True)

    def __init__(self, email):
        """initialize with name."""
        self.email = email


    def __repr__(self):
        return "<User: {}>".format(self.email)
