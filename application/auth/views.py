from flask import g, jsonify, request
from flask_httpauth import HTTPTokenAuth
from flask_login import logout_user
from application.auth.model import User
from flask_restful import abort, Resource
from manage import db
import boto3, json

auths = HTTPTokenAuth(scheme='Token')
def upload(url):
    aws_access_key_id = 'so'
    aws_secret_access_key = 'so'
    pass

class Register(Resource):
    @auths.verify_token
    def verify_token(self,token):
        # authenticate by token only
        user = User.verify_auth_token(token)
        if not user:
            return False
        g.user = user
        return True

    def post(self):
        """Register a user"""
        try:
            name = request.json.get('name')
            email = request.json.get('email')
            password = request.json.get('password')
            passport = request.json.get('passport')
            if email is "Null" or password is "Null" or name is "Null":
                return ('missing name, email or password!')
            if len(password) >= 6:
                if db.session.query(User).filter_by(email=email).first() is not None:
                    return ("This user already exists!")
                if passport:
                    user = User(name=name, email=email, password=password, passport=passport)
                else:
                    user = User(name=name, email=email, password=password, passport='www.hot.com')
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                return ("Successfully registered {0}".format(email))
            else:
                return ('password characters shouold be more than six! Please try again!')
        except:
            return 'please enter your name, email, password and path to your passport picture'

class Login(Resource):
    def post(self):
        try:

            email = request.json.get('email')
            password = request.json.get('password')

            if email is None or password is None:
                return ('missing arguments!')

            user = db.session.query(User).filter_by(email=email).first()
            if not user:
                return ("error! {0} is not registered".format(email))
            elif user and not user.check_password(password):
                return ("error! Invalid password")
            else:
                token = user.generate_auth_token()
                return ({'Authorization': token.decode('ascii')})
                # return jsonify(message="login succesfull! \n token : {}".format(token), token=token.decode()), 302
        except:
            return 'please enter your email and password to login'


    def get(self):
          return 'please enter your email and password to login'

    @auths.login_required
    def logout(self):
        logout_user()
        return ("Logout succesfull")


class Index(Resource):
      def get(self):
            data = {
              "WELCOME TO AIRTECH!!!!":{
                "Use the following URLs to begin your journey":{
                  "urls":{
                    "register":"/auth/register",
                    "login":"/auth/login"
                    }
            }}}
            return data
