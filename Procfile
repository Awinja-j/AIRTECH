web: gunicorn run:app
web: locust -P 8089
init: python manage.py db init
migrate: python manage.py migrate
upgrade: python mentorbot.manage.py upgrade
