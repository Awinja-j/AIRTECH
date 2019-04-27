import os, uuid
import smtplib
import datetime
from flask import g, jsonify, request
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from flask_restful import abort, Resource
from manage import db
from application.book.model import Booking, Email
from application.book.flights import flight_details
from collections import Counter
from application.book.email_templates import reminder, reservation_confirmation, booking_confirmation

class Book(Resource):
    '''------------------------send emails------------------------'''
    login = os.environ.get("LOGIN")
    password = os.environ.get("PASSWORD")
    from_addr = os.environ.get("FROM_ADDRESS")
    smtpserver ='smtp.gmail.com:587'

    def check_email_type(self, email_type, customer, date, seat):
        if email_type is 'reminder':
            return reminder.format(customer)
        if email_type is 'reserved':
              return reservation_confirmation.format(customer)
        if email_type is 'booked':
              return booking_confirmation.format(customer)

    def sendemail(self, to_addr_list, subject, date, seat):
        try:
            header  = 'From: %s\n' % self.from_addr
            header += 'To: %s\n' % ','.join(to_addr_list)
            header += 'Subject: %s\n\n' % subject
            message = header + check_email_type(subject, to_addr_list, date, seat)

            server = smtplib.SMTP(self.smtpserver)
            server.starttls()
            server.login(login, password)
            problems = server.sendmail(from_addr, to_addr_list, message)
            server.quit()
            return
        except:
            return 'something went wrong'


    '''----------------------------pay for a seat-------------------------'''
    airports = ["nairobi", "kampala", "mombasa", "kigali", "windhoek", "kakamega"]
    available_seats = []
    booked = {} #get this data from the db

    def check_airports(self, airport_name):
          for key, value in flight_details.items():
                return


    def find_flight(self, depature, destination):
        '''this returns flight details when a flight has free space'''
        for plane_type, plane_details in flight_details.items():
          print(depature.lower(), destination.lower())
          if depature and destination in plane_details['destinations']:
              booked = Counter(self.booked)
              for key, value in booked.items():
                if key == plane_type:
                  if value < plane_details['capacity']:
                      return plane_type, plane_details

    def generate_seat_number(self, destination, depature):
        """ generates a seat number """
        flight_info = self.find_flight(destination, depature)
        if flight_info is None:
              return "That flight is fully booked"

    def check_if_seat_number_is_available(self, seat_number):
          return seat_number

    def check_ticket_status(self, ticket_status):
          '''checks if ticket status is booked or reserved'''
          try:
              ticket_status.lower()
              if ticket_status is 'booked' or 'reserved':
                return ticket_status
              else:
                return 'This is not a valid ticket status, Booked or Reserved'
          except:
                return  'please add ticket status, Booked or Reserved'

    def check_mpesa_code(self, mpesa_code):
        '''does everything mpesa'''
        try:
            if len(mpesa_code) == 12:
              return mpesa_code
            else:
              return 'mpesa code should be 12 digits long'
        except:
            return 'Mpesa code is missing. Please add one'

    def check_trip_type(self, trip_type):
          '''checks trip type if it is return or one way'''
          try:
              trip_type.lower()
              if trip_type is 'return' or trip_type is 'one way':
                  return trip_type
              else:
                  return 'This is not a valid trip type, Return or One way'
          except:
                return 'Please enter your trip type, Return or One way'

    def check_date_is_not_past(date):
        '''this returns false if the date is in the past'''
        present = datetime.now()
        d1 = datetime.strptime(date, "%d/%m/%Y")
        return present < d1

    def check_depature_time_and_date(self, depature_date):
          try:
            time = check_date_is_not_past(depature_date)
            if time is True:
                return depature_date
            else:
                return 'Please enter a date that is present or in the future'
          except:
              return "when do you plan to travel? please enter a depature date"

    def check_return_time_and_date(self, return_date):
          try:
            time = check_date_is_not_past(return_date)
            if time is True:
                return return_date
            else:
                return 'Please enter a date that is present or in the future'
          except:
              return "when do you plan to return? please enter a return date"

    def check_if_details_are_right(self, details):

        return details

    def reserve(self, trip_type, depature_date, return_date, seat_number, depature, destination):
        seat_number = self.check_if_seat_number_is_available(seat_number)
        depature = self.check_airports(depature)
        destination = self.check_airports(destination)
        depature_date = self.check_depature_time_and_date(depature_date)
        trip_type = self.check_trip_type(trip_type)
        if trip_type is 'one way':
              return_date = None
        if trip_type is 'return':
              try:
                  return_date = self.check_return_time_and_date(return_date)
              except:
                  return "Return trips must have a return date"

        details={
                    "ticket_status":"reserved",
                    "trip_type":trip_type,
                    "depature":depature,
                    "destination":destination,
                    "seat_number":seat_number,
                    "depature_date":depature_date,
                    "return_date":return_date,
          }
        return details

    def booked(self, seat_number, mpesa_code, trip_type, depature, destination, depature_date, return_date):
        seat_number = self.check_if_seat_number_is_available(seat_number)
        mpesa_code = self.check_mpesa_code(mpesa_code)
        trip_type = self.check_trip_type(trip_type)
        depature = self.check_airports(depature)
        destination = self.check_airports(destination)
        depature_date = self.check_depature_time_and_date(depature_date)

        if trip_type is 'one way':
              return_date = None
        if trip_type is 'return':
              try:
                return_date = self.check_return_time_and_date(return_date)
              except:
                  return "Return trips must have a return date"
        details={
                    "ticket_status":"booked",
                    "trip_type":trip_type,
                    "depature":depature,
                    "destination":destination,
                    "seat_number":seat_number,
                    "depature_date":depature_date,
                    "return_date":return_date,
                    "mpesa_code":mpesa_code
          }
        return details

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

        seat_number = request.json.get('seat_number')
        ticket_status = request.json.get('ticket_status')
        mpesa_code = request.json.get('mpesa_code')
        trip_type = request.json.get('trip_type')
        depature = request.json.get('depature')
        destination = request.json.get('destination')
        depature_date = request.json.get('depature_date')
        return_date = request.json.get('return_date')


        try:
            if ticket_status is 'reserved':
                  details = self.reserve(trip_type, depature_date, return_date, seat_number, depature, destination)

            if ticket_status is 'booked':
                  details = self.booked(seat_number, mpesa_code, trip_type, depature, destination, depature_date, return_date)

            booking = Booking(details)

            db.session.add(booking)
            db.session.commit()
            self.sendemail() # to fix
            return ("Seat number{0}{}succesfully".format(seat_number, trip_type))

        except:
          return("enter your booking details!")

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
          try:
            destination = request.args.get('destination')
            destination = self.check_airports(destination)
            empty_seats = Booking.query.filter_by(destination=destination)
            return empty_seats
          except:
            return 'Some sort of error'

class Get_reserved_seats(Resource):
      def get(Resource):
          '''will only return reserved seats'''
          reserved = Booking.query.filter_by(ticket_status='reserved').all()
          return reserved

# class Scheduler(Resource):
#       '''schedules events'''

#       def get():
#           jobstores = {
#               'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
#           }
#           executors = {
#               'default': ThreadPoolExecutor(20),
#               'processpool': ProcessPoolExecutor(5)
#           }
#           job_defaults = {
#               'coalesce': False,
#               'max_instances': 3
#           }
#           scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

#       def check_day_before():
#             id = 1
#             to_addr_list = 'jojo@gmail.com'
#             subject = 'reminder'
#             date = '12/03/2019'
#             seat = '2d'
#             return id, to_addr_list, subject, date, seat

#       id, to_addr_list, subject, date, seat = check_day_before()

#       Scheduler.add_job(Email.sendemail(to_addr_list, subject, date, seat), 'interval', minutes=2, id=id)
#       Scheduler.start()
