from email.views import sendemail
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


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

def book():
      return 'funtimes'

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
