web: gunicorn run:app
web: locust -P 8089 --host=https://airtech-j.herokuapp.com
init: python manage.py db init
migrate: python manage.py migrate
upgrade: python mentorbot.manage.py upgrade
