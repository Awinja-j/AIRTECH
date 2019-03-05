import uuid
from datetime import datetime
from manage import app, db
from application.auth.model import User


class Booking(db.Model):
    __tablename__ = "booking"
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    aircraft_id = db.Column(db.String(255), nullable=False)
    seat_number = db.Column(db.String(255), nullable=False, unique=True)
    ticket_status = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, email):
        """initialize with name."""
        self.email = email

    def __repr__(self):
        return "<User: {}>".format(self.email)

    def generate_plane_details(self):
          return
    def generate_seat_number(self):
        num = uuid.uuid4()
        return "{}{}".format('AIRTECH-S',num)

class Ticket(db.Model):
    __tablename__ = "ticket"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    client_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    aircraft_id = db.Column(db.String(255), nullable=False, unique=True)
    seat_id = db.Column(db.String(255), nullable=False, unique=True)
    created_on = db.Column(db.DateTime, nullable=False)
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, email):
        """initialize with name."""
        self.email = email

    def __repr__(self):
        return "<User: {}>".format(self.email)

    def generate_amount(self):
          pass

class Reserve(db.Model):
      __tablename__ = "reserve"
      id = db.Column(db.Integer, primary_key=True)
      client_id = db.Column(db.Integer, db.ForeignKey("user.id"))
      booking_id = db.Column(db.Integer, db.ForeignKey("booking.id"))
      seat_number = db.Column(db.String(255), nullable=False, unique=True)

      def __init__(self, email):
        """initialize with name."""
        self.email = email

      def __repr__(self):
        return "<User: {}>".format(self.email)



class Payment(db.Model):
    __tablename__ = "payment"
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("user.id"))


    def __init__(self, email):
        """initialize with name."""
        self.email = email


    def __repr__(self):
        return "<User: {}>".format(self.email)
