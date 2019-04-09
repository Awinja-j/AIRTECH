import os, uuid
import smtplib
from flask import g, jsonify, request
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from flask_restful import abort, Resource
from manage import db
from application.book.model import Booking, Email



# jobstores = {
#     'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
# }
# executors = {
#     'default': ThreadPoolExecutor(20),
#     'processpool': ProcessPoolExecutor(5)
# }
# job_defaults = {
#     'coalesce': False,
#     'max_instances': 3
# }
# scheduler = BackgroundScheduler()

# def check_day_before():
#       id = 1
#       to_addr_list = 'jojo@gmail.com'
#       subject = 'reminder'
#       date = '12/03/2019'
#       seat = '2d'
#       return id, to_addr_list, subject, date, seat

# id, to_addr_list, subject, date, seat = check_day_before()

# scheduler.add_job(sendemail(to_addr_list, subject, date, seat), 'interval', minutes=2, id=id)
# scheduler.start()

class Book(Resource):
    '''pay for a seat'''
    airports = ["nairobi", "kampala", "mombasa", "kigali", "windhoek", "kakamega"]

    def generate_flight_number(self):
        num = uuid.uuid4()
        return "{}{}".format('AIRTECH-S',num)

    def get(self):
        '''check the details of your flight using  the seat number'''
        seat_number = request.args.get('seat_number')
        if not seat_number:
              return 'please provide your seat number'
        my_details = db.session.query(Booking).filter_by(seat_number=seat_number)
        #ToFix: how do we know the one searching is the owner of the seat?, check person searchin's id and
        # return details only if the user email(person should be logged in) in ticker and person searching are the same
        return my_details

    def post(self):
        '''book a seat'''

        # client_id = 1
        seat_number = request.json.get('seat_number')
        ticket_status = request.json.get('ticket_status')
        mpesa_code = request.json.get('mpesa_code')
        trip_type = request.json.get('trip_type')
        depature = request.json.get('depature')
        destination = request.json.get('destination')
        depature_date = request.json.get('depature_date')
        return_date = request.json.get('return_date')

        #ToFix: Booking for a past date
        #ToFix: Booking without a seat number, generate seat number for them
        #ToFix: Reserve without a seat number, generate seat number for them
        #Tofix: Book with missing ticket status, assume reserve of mpesa is missing
        #Tofix: Book with missing ticket status, assume booked if mpesa is available
        #ToFix: user can reserve without a seat number.
        #to fix: user must enter destination/depature for both booking and reserve
        # missing return date/ depature date
        if not depature_date:
          return "when do you plan to travel?"
        else:
            # empty_seats = db.session.query(Booking).filter_by(seat_number=seat_number)
            # empty_seats = Booking.query.get(seat_number)
            # if seat_number not in empty_seats:
            #     return 'Sorry that seat is taken' #should give a list of available seats

            if trip_type == "return" and not return_date:
                return "round trips must have a return date"

            if ticket_status == "booked" and not mpesa_code:
                  return "Your ticket status is Booked with Mpesa code is missing. Please add one"

            if depature not in self.airports:
                  return "We are currently not in that location"

            if destination not in self.airports:
                  return "We currently do not fly to that location"

            flight_number = self.generate_flight_number()
            if trip_type is "reserve":
                  flight_number = "reserve"

            booking = Booking(client_id=client_id,
                              ticket_status=ticket_status,
                              flight_number=flight_number,
                              trip_type = trip_type,
                              depature=depature,
                              destination=destination,
                              seat_number=seat_number,
                              depature_date=depature_date,
                              return_date=return_date,
                              mpesa_code=mpesa_code
                              )

            db.session.add(booking)
            db.session.commit()
            return ("Seat number{0} booked succesfully".format(seat_number))

        # try:

        # except:
        #   return("enter your booking details!")


class Get_All(Resource):
      '''get a list of all the flight destinations'''
      def get(self):
            data = {
              "WELCOME TO AIRTECH!!!!":{
                "Here is a list of the destinations we currenly serve":
                  {
                    "Kenya",
                    "Morocco",
                    "Tanzania",
                    "Dubai",
                    "Angola",
                    "Mozambique"
                  },
                "More Details": { "20 seats in each plane", "numbered 1-20"}
            }}
            return data

class Get_empty_seats(Resource):
      '''get a list of all empty seats available in the destination you are going'''
      def get(self):
          destination = request.args.get('destination')
          if not destination:
              return 'where are you going?'
          x = ["kenya", "morocco", "tanzania", "dubai", "angola", "mozambique"]
          if destination not in x:
              return 'we may not be going to that destination!'
          availability = db.session.query(Booking).filter_by(destination=destination)
          return availability
                # return "funtimes"
          # for x in availability:
          #   for y in range(20):
          #       if x != y:
          #         return y

class Get_reserved_seats(Resource):
      def get(Resource):
            '''will only return reserved seats'''
            flight_number = request.args.get('flight_number')
            depature_date = request.args.get('depature_date')
            pass

login = os.environ.get("LOGIN")
password = os.environ.get("PASSWORD")
from_addr = os.environ.get("FROM_ADDRESS")
smtpserver ='smtp.gmail.com:587'


class Email(Resource):
    '''send email'''

    def email_type(self, type, customer, date, seat):
        if type is 'reminder':
            return 'Dear {}'.format(customer)
        else:
            return 'Dear {}'.format(customer)

    def sendemail(self, to_addr_list, subject, date, seat):
        # header  = 'From: %s\n' % from_addr
        # header += 'To: %s\n' % ','.join(to_addr_list)
        # header += 'Subject: %s\n\n' % subject
        # message = header + email_type(subject, to_addr_list, date, seat )

        # server = smtplib.SMTP(smtpserver)
        # server.starttls()
        # server.login(login,password)
        # problems = server.sendmail(from_addr, to_addr_list, message)
        # server.quit()
        return 'problems'

    def get(self):
        return 'just get man!'
