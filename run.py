import os
from flask_script import Manager
from flask_restful import Api
from config import DevelopmentConfig
from application.auth.views import Register, Login, Index, Profile, Logout
from application.book.views import Book, Email, Get_All, Get_empty_seats, Get_reserved_seats
from application.auth.model import User
from application.book.model import Booking, Email
from manage import app, db

api = Api(app)

with app.app_context():
    from application.auth.model import User
    from application.book.model import Booking, Email
    db.init_app(app)
    db.create_all()

# app.config.from_object(os.environ['APP_SETTINGS'])
app.config.from_object(DevelopmentConfig)
api.add_resource(Register, '/auth/register')
api.add_resource(Login, '/auth/login')
api.add_resource(Logout, '/auth/logout')
api.add_resource(Index, '/')
api.add_resource(Profile, '/auth/profile')
api.add_resource(Book, '/api/book')
api.add_resource(Get_reserved_seats, '/api/get_reserved_seats')
api.add_resource(Get_All, '/api/get_all')
api.add_resource(Get_empty_seats, '/api/get_empty_seats')

manager = Manager(app)

if __name__ == '__main__':
    app.run(debug=True)
