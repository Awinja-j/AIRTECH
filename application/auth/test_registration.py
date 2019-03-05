import unittest
from manage import app, db
from config import TestingConfig
import json

class RegistrationTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.app.config.from_object(TestingConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def register_user(self, email="joan.awinja@andela.com", password="Awinja@1"):
        user = {
            "email": email,
            "password": password
        }
        return self.client.post('/auth/register', data=json.dumps(user), content_type='application/json')

    def test_succesful_user_registration(self):
        """This tests sucessful user registration"""
        email = "jane.awinja@andela.com"
        password = "Awinja@1"
        user = {"email": email, "password": password }
        response = self.client.post('/auth/register', data=json.dumps(user), headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 201)

    def test_registration_with_empty_password_field(self):
        """This tests registering a user with missing password"""
        user = {"email": "judy.khasoa@andela.com", "password": " "}
        response = self.client.post('/auth/register', data=user, headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_register_with_empty_email_field(self):
        """This tests registering a user with missing email"""
        user = {"email": " ", "password": "Nganyi@1"}
        response = self.client.post('/auth/register', data=user, headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_registration_with_invalid_email_format(self):
        """This tests registering a user with invalid email format"""
        user = {"email": "james.ochweri.com", "password": "Ochweri@1"}
        response = self.client.post('/auth/register', data=user, headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_registration_with_used_email_address(self):
        """This tests registering a user multiple times"""
        user = {"email": "joan.awinja@andela.com", "password": "Awinja@1"}
        response = self.client.post('/auth/register', data=user, headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
            """teardown all initialized variables."""
            with self.app.app_context():
                # drop all tables
                db.session.remove()
                db.drop_all()

    # Make the tests conveniently executable
    if __name__ == "__main__":
        unittest.main()
