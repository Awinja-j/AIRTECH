web: gunicorn run:app
locust: locust -P 8089 --host=https://airtech-j.herokuapp.com -f locust.py
init: python manage.py db init
migrate: python manage.py migrate
upgrade: python mentorbot.manage.py upgrade
