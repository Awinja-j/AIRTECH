from flask import g, jsonify, request
from email.views import sendemail
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from flask_restful import abort, Resource
from manage import db
from model import Reserve, Ticket, Payment, Booking



jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
scheduler = BackgroundScheduler()

def check_day_before():
      id = 1
      to_addr_list = 'jojo@gmail.com'
      subject = 'reminder'
      date = '12/03/2019'
      seat = '2d'
      return id, to_addr_list, subject, date, seat

id, to_addr_list, subject, date, seat = check_day_before()

scheduler.add_job(sendemail(to_addr_list, subject, date, seat), 'interval', minutes=2, id=id)
scheduler.start()
class Book(Resource):
    def book():
      return 'funtimes'
    def get():
          pass
    def post():
          pass


class Reserve_(Resource):

    def generate_flight_details(self):
        '''this generates flight details like plane number'''
        pass

    def post(self, request):
        '''this function reserves a seat for users'''
        client_id =
        date_of_travel = request.json.get('date_of_travel')
        destination = request.json.get('destination')
        depature = request.json.get('depature)
        flight_ number, seat_number = self.generate_flight_detailsgenerate(date_of_travel)

    def get(self, request):
        '''this checks how many people have made reservations for a particular flight on a specific day'''
        details = []
        if not request.json:
            return ("No JSON file detected.")
        flight = request.json.get('flight')
        day = request.json.get('day')
        if not flight or day:
              return jsonify(message='please specify flight or travel date'), 400
        if flight and not day:
              reservation = db.session.query(Reserve).filter_by(light_number=flight)
              details.append(reservation)
        if day and not flight:
              reservation = db.session.query(Reserve).filter_by(date_of_travel=day)
              details.append(reservation)
        if flight and day:
            reservation = db.session.query(Reserve).filter_by(light_number=flight, date_of_travel=day)
            details.append(reservation)
        return details
