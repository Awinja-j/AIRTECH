import uuid
from datetime import datetime
from manage import app, db
from application.auth.model import User


class Booking(db.Model):
    '''contains seats that have been paid for plus flight details and amount'''
    __tablename__ = "booking"
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    flight_number = db.Column(db.String(255), nullable=False)
    seat_number = db.Column(db.String(255), nullable=False, unique=True)
    ticket_status = db.Column(db.String(255), nullable=False) # booked or reserved
    trip_type = db.Column(db.String(255), nullable=False) #one way or return trip
    mpesa_code = db.Column(db.String(255), nullable=True)
    depature = db.Column(db.String(255), nullable=False) #the place they are leaving
    destination = db.Column(db.String(255), nullable=False) #the place they are going to
    depature_date = db.Column(db.String(255), nullable=False) #the day the user is leaving
    return_date = db.Column(db.String(255), nullable=True) #if return, the date the user is coming back
    created_on = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, client_id, flight_number, seat_number, ticket_status, trip_type, mpesa_code, depature, destination, depature_date, return_date):
        """initialize with name."""
        self.client_id = client_id
        self.flight_number = flight_number
        self.seat_number = seat_number
        self.ticket_status = ticket_status
        self.trip_type = trip_type
        self.mpesa_code = mpesa_code
        self.depature = depature
        self.destination = destination
        self.depature_date = depature_date
        self.return_date = return_date

    def __repr__(self):
        return "<Booking: {}>".format(self.seat_number)

class Email(db.Model):
    '''contains details of all emails sent'''
    id = db.Column(db.Integer, primary_key=True)
    to_addr_list = db.Column(db.String(80), unique=True, nullable=False)
    cc_addr_list = db.Column(db.String(120), unique=True, nullable=False)
    subject = db.Column(db.String(80), unique=True, nullable=False)
    message = db.Column(db.Text, unique=True, nullable=False)

    def __repr__(self):
        return '<Email %r>' % self.message
