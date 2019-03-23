from datetime import datetime
from werkzeug.security import generate_password_hash, \
     check_password_hash
from flask_login import UserMixin
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from manage import app, db
import boto3


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    passport = db.Column(db.String(1024), nullable=True)
    created_on = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


    def __init__(self, name, email, password, passport):
        """initialize with name."""
        self.name = name
        self.email = email
        self.set_password(password)
        self.registered_on = datetime.now()
        self.passport = upload(passport)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self, expiration=3600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    def upload(self, passport):
        s3 = boto3.client('s3')
        filename = passport
        bucket_name = app.config['BUCKET_NAME']
        s3.upload_file(filename, bucket_name, filename)

    def delete(self, passport):
          pass

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return "expired" # valid token, but expired
        except BadSignature:
            return "bad token"  # invalid token
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
