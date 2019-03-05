from datetime import datetime
from werkzeug.security import generate_password_hash, \
     check_password_hash
from flask_login import UserMixin
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from manage import app, db, bcrypt


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    passport = db.relationship('passport', backref='user', lazy='dynamic')
    created_on = db.Column(db.DateTime, nullable=False)
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


    def __init__(self, name, email, password):
        """initialize with name."""
        self.name = name
        self.email = email
        self.set_password(password)
        self.registered_on = datetime.datetime.now()

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self, expiration=3600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        # s = Serializer(os.getenv('SECRET_KEY'), expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user


    def __repr__(self):
        return "<User: {}>".format(self.email)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return User.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Passport(db.Model):
      __tablename__ = "passport"
      id = db.Column(db.Integer, primary_key=True)
      url = db.Column(db.String(255), nullable=True)
      user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
      created_on = db.Column(db.DateTime, nullable=False)
      date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

      def __init__(self, url):
            self.url = url

      def __repr__(self):
            return "<passport: {}>".format(self.url)
