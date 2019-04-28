web: gunicorn run:app
web: cd application/auth && locust --host=https://airtech-j.herokuapp.com
init: python manage.py db init
migrate: python manage.py migrate
upgrade: python mentorbot.manage.py upgrade
