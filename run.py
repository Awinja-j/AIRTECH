from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from application.auth.views import Register, Login

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
CORS(app)

api.add_resource(Register, '/auth/register')
api.add_resource(Login, '/auth/login')
api.add_resource(Login, '/auth/logout')

if __name__ == '__main__':
    app.run(debug=True)
