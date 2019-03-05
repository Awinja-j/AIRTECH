from flask import g, jsonify, request
from flask_httpauth import HTTPTokenAuth
from flask_login import logout_user
from application.auth.model import User
from flask_restful import abort, Resource
from manage import db

auths = HTTPTokenAuth(scheme='Token')

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
            if email is None or password is None or name is None:
                return jsonify(message='missing name, email or password!'), 400
            if len(password) > 6:
                if db.session.query(User).filter_by(email=email).first() is not None:
                    return jsonify(message=' This user already exists!'), 400
                if passport:
                    user = User(name=name, email=email, password=password, passport=passport)
                user = User(name=name, email=email, password=password, passport='www.hot.com')
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                return jsonify(message="Successfully registered {0}".format(email)), 201
            else:
                return jsonify(message='password characters shouold be more than six! Please try again!'), 404
        except AttributeError:
            return 'enter something man!'

class Login(Resource):
    def post(self):
        if not request.json:
            return ("No JSON file detected.")

        email = request.json.get('email')
        password = request.json.get('password')

        if email is None or password is None:
            return jsonify(message='missing arguments!'), 400

        user = db.session.query(User).filter_by(email=email).first()
        if not user:
            return jsonify(message="error! {0} is not registered".format(email)), 400
        elif user and not user.check_password(password):
            return jsonify(message="error! Invalid password"), 403
        else:
            token = user.generate_auth_token()
            return jsonify({'Authorization': token.decode('ascii')}), 200
            # return jsonify(message="login succesfull! \n token : {}".format(token), token=token.decode()), 302

    def get(self):
          return 'please enter your email and password to login'

    @auths.login_required
    def logout(self):
        logout_user()
        return jsonify(message="Logout succesfull")
