from flask import g, jsonify, request, redirect, url_for
from flask_httpauth import HTTPTokenAuth
from flask_login import logout_user
from application.auth.model import User
from flask_restful import abort, Resource
from manage import db, app
import json
import re

auths = HTTPTokenAuth(scheme='Token')

@auths.verify_token
def verify_token(token):
    # authenticate by token only
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True

class Register(Resource):
    '''checks if email is valid'''
    def isValidEmail(email):
      if len(email)>7:
          m = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
          if m == None:
              return False
          else:
              return True
      else:
          return False

    def is_password_strong(password):
        length_regex = re.compile(r'.{8,}')
        uppercase_regex = re.compile(r'[A-Z]')
        lowercase_regex = re.compile(r'[a-z]')
        digit_regex = re.compile(r'[0-9]')

        return (length_regex.search(password) is not None
                and uppercase_regex.search(password) is not None
                and lowercase_regex.search(password) is not None
                and digit_regex.search(password) is not None)

    def post(self):
        """Register a user"""
        try:
            name = request.json.get('name')
            email = request.json.get('email')
            password = request.json.get('password')
            passport = request.json.get('passport')
            if email is "Null" or password is "Null" or name is "Null":
                return ('missing name, email or password!')
            if self.isValidEmail is False:
                  return ("This is not a valid email address")
            if self.is_password_strong() is False:
                  return "Please enter a strong password"
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
                return ({'Authorization': token.decode()})
        except:
            return 'please enter your email and password to login'

    def get(self):
          return 'please enter your email and password to login'

class Logout(Resource):
       def get(self):
            token = request.headers.get('Authorization')
            if token:
                user_id = verify_token(token)
                if user_id:
                    logout_user()
                    return redirect(url_for('index'))

class Profile(Resource):

      def get(self):
        token = request.headers.get('Authorization')
        if token:
            user_id = verify_token(token)
            if user_id:
                return 'you can view your details here'
            else:
                return 'no token'

      def delete(self):
        token = request.headers.get('Authorization')
        if token:
          user_id = verify_token(token)
          if user_id:
              try:
                email = request.json.get('email')
                password = request.json.get('password')

                user = User.query.get(email=email)
                if not user or user.email != g.user.email:
                      return "email not found"
                else:
                      db.session.delete(user)
                      db.session.commit()
                      return 'profile deleted succesfully'
              except:
                return 'what is your email address?'

      def put(self):
          token = request.headers.get('Authorization')
          if token:
              user_id = verify_token(token)
              if user_id:
                  try:
                    email = request.json.get('email')
                    user = User.query.get(email=email)

                    if not user or user.email != g.user.email:
                          return "email not found"

                    if request.json.get('name'):
                      user.name = request.json.get('name')
                    if request.json.get('password'):
                      user.password = request.json.get('password')
                    if request.json.get('passport'):
                      user.passport = request.json.get('passport')

                  except:
                    return 'what is your email address?'



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
