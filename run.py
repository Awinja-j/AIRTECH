import os
from flask_script import Manager
from flask_restful import Api
from config import DevelopmentConfig
from application.auth.views import Register, Login, Index, Profile
from application.book.views import Book, Reserve, Email, Get_All, Get_empty_seats
from application.auth.model import User
# from application.book.model import Book
from application.email.model import sent_email
# from application.reserve.model import Reserve
from manage import app, db

api = Api(app)

with app.app_context():
    from application.auth.model import User
    from application.email.model import sent_email
    # from app.models import User, sent_email
    db.init_app(app)
    db.create_all()

# app.config.from_object(os.environ['APP_SETTINGS'])
app.config.from_object(DevelopmentConfig)
api.add_resource(Register, '/auth/register')
api.add_resource(Login, '/auth/login')
api.add_resource(Login, '/auth/logout')
api.add_resource(Index, '/')
api.add_resource(Profile, '/auth/profile')
api.add_resource(Profile, '/api/book')
api.add_resource(Profile, '/api/reserve')
api.add_resource(Profile, '/api/email')
api.add_resource(Profile, '/api/get_all')
api.add_resource(Profile, '/api/get_empty_seats')

manager = Manager(app)

if __name__ == '__main__':
    app.run(debug=True)
