import unittest

from application.auth.manage import db, app

class BookingTestCase(unittest.TestCase):
      '''This tests the booking functionality'''
      def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.app.config.from_object(TestingConfig)
        self.client = self.app.test_client()
        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

      def register_user(self, email="joan.awinja@andela.com", password="Awinja@1"):
          user = {
          "email": email,
          "password": password
          }
          return self.client.post('/auth/register', data=json.dumps(user), content_type='application/json')

      def login_user(self, email="joan.awinja@andela.com", password="Awinja@1"):
          user = {
          "email": email,
          "password": password
          }
          return self.client.post('/auth/login', data=json.dumps(user), content_type='application/json')

      def book_a_seat(self):
          self.register_user()
          result = self.login_user()
          token = json.loads(result.get_data(as_text=True))['Authorization']

          book = {
              "seat_number":1,
              "mpesa_code": "hdjhhjkdsjkkjs",
              "ticket_status": "booked",
              "trip_type": "return",
              "depature": "kenya",
              "destination": "kampala",
              "depature_date":"12-04-2019",
              "return_date":"12-04-2019"
            }
          return self.client.post('/api/book', data=json.dumps(book), headers={'Content-Type': 'application/json','Authorization': token})

      def reserve_a_seat(self):
            self.register_user()
            result = self.login_user()
            token = json.loads(result.get_data(as_text=True))['Authorization']

            reserve = {
                "seat_number":2,
                "ticket_status": "reserved",
                "trip_type": "return",
                "depature": "kenya",
                "destination": "kampala",
                "depature_date":"12-04-2019",
                "return_date":"12-04-2019"
              }
            return self.client.post('/api/book', data=json.dumps(reserve), headers={'Content-Type': 'application/json','Authorization': token})

      def test_check_flight_details(self):
          '''tests checking of user flight tickets functionality'''
          self.register_user()
          result = self.login_user()
          token = json.loads(result.get_data(as_text=True))['Authorization']

          params = {"seat_number":2}
          response = self.client.get('/api/book', data=params, headers={'Content-Type': 'application/json','Authorization': token})
          self.assertIn('seat_number' , str(response.data))

      def test_check_flight_details_missing_seat_number(self):
          '''tests checking of user flight tickets functionality with missing flight number'''
          self.register_user()
          result = self.login_user()
          token = json.loads(result.get_data(as_text=True))['Authorization']

          params = {"seat_number":""}
          response = self.client.get('/api/book', data=params, headers={'Content-Type': 'application/json','Authorization': token})
          self.assertIn('please provide your seat number' , str(response.data))

      def test_check_flight_details_unavailable_seat_number(self):
          '''tests checking of user flight tickets functionality with wrong flight number'''
          self.register_user()
          result = self.login_user()
          token = json.loads(result.get_data(as_text=True))['Authorization']

          params = {"seat_number":"100"}
          response = self.client.get('/api/book', data=params, headers={'Content-Type': 'application/json','Authorization': token})
          self.assertIn('please provide your seat number' , str(response.data))
#booking
      def test_booking(self):
          '''test booking succesfully'''
          response = self.book_a_seat()
          self.assertEqual(response.status_code, 201)

      def test_booking_missing_mpesa_code(self):
          '''test booking functionality with missing mpesa code'''
          self.register_user()
          result = self.login_user()
          token = json.loads(result.get_data(as_text=True))['Authorization']

          book = {
                "seat_number":4,
                "ticket_status": "booked",
                "trip_type": "return",
                "depature": "kenya",
                "destination": "kampala",
                "depature_date":"12-04-2019",
                "return_date":"12-04-2019"
              }
          response = self.client.get('/api/book', data=book, headers={'Content-Type': 'application/json','Authorization': token})
          self.assertIn('Your ticket status is Booked with Mpesa code is missing. Please add one', str(response.data))

      def test_booking_missing_destination(self):
          '''test booking with missing destination'''
          self.register_user()
          result = self.login_user()
          token = json.loads(result.get_data(as_text=True))['Authorization']

          book = {
                "seat_number":9,
                "mpesa_code": "hdjhhjkdsjkkjs",
                "ticket_status": "booked",
                "trip_type": "return",
                "depature": "kakamega",
                "depature_date":"12-04-2019",
                "return_date":"12-04-2019"
              }
          response = self.client.get('/api/book', data=book, headers={'Content-Type': 'application/json','Authorization': token})
          self.assertIn('Please enter your destination', str(response.data))

      def test_booking_missing_depature(self):
          '''test rbooking with missing depature'''
          self.register_user()
          result = self.login_user()
          token = json.loads(result.get_data(as_text=True))['Authorization']

          rbook = {
                "seat_number":5,
                "mpesa_code": "hdjhhjkdsjkkjs",
                "ticket_status": "booked",
                "trip_type": "return",
                "destination": "eldoret",
                "depature_date":"12-04-2019",
                "return_date":"12-04-2019"
              }
          response = self.client.get('/api/book', data=book, headers={'Content-Type': 'application/json','Authorization': token})
          self.assertIn('Please enter your depature', str(response.data))

      def test_booking_missing_depature_date(self):
          '''test reserving with missing depature date'''
          self.register_user()
          result = self.login_user()
          token = json.loads(result.get_data(as_text=True))['Authorization']

          book = {
                "seat_number":5,
                "mpesa_code": "hdjhhjkdsjkkjs",
                "ticket_status": "booked",
                "trip_type": "return",
                "destination": "mombasa",
                "depature": "kampala",
                "return_date":"12-04-2019"
              }
          response = self.client.get('/api/book', data=book, headers={'Content-Type': 'application/json','Authorization': token})
          self.assertIn('Please enter your depature date', str(response.data))

      def test_booking_missing_return_date(self):
          '''test reserving with missing return date'''
          self.register_user()
          result = self.login_user()
          token = json.loads(result.get_data(as_text=True))['Authorization']

          book = {
                "seat_number":5,
                "mpesa_code": "hdjhhjkdsjkkjs",
                "ticket_status": "booked",
                "trip_type": "return",
                "destination": "mombasa",
                "depature": "kampala",
                "depature_date":"12-04-2019"
              }
          response = self.client.get('/api/book', data=book, headers={'Content-Type': 'application/json','Authorization': token})
          self.assertIn('Please enter your return date', str(response.data))

      def test_booking_a_past_depature_date(self):
            '''test booking a past date'''
            self.register_user()
            result = self.login_user()
            token = json.loads(result.get_data(as_text=True))['Authorization']

            book = {
                "seat_number":1,
                "mpesa_code": "hdjhhjkdsjkkjs",
                "ticket_status": "booked",
                "trip_type": "return",
                "depature": "kenya",
                "destination": "kampala",
                "depature_date":"12-04-2017",
                "return_date":"12-04-2019"
              }
            response = self.client.post('/api/book', data=json.dumps(book), headers={'Content-Type': 'application/json','Authorization': token})
            self.assertIn('Please enter a valid depature date', str(response.data))
      def test_booking_a_past_return_date(self):
            '''test booking a past date'''
            self.register_user()
            result = self.login_user()
            token = json.loads(result.get_data(as_text=True))['Authorization']

            book = {
                "seat_number":1,
                "mpesa_code": "hdjhhjkdsjkkjs",
                "ticket_status": "booked",
                "trip_type": "return",
                "depature": "kenya",
                "destination": "kampala",
                "depature_date":"12-04-2019",
                "return_date":"12-04-2010"
              }
            response = self.client.post('/api/book', data=json.dumps(book), headers={'Content-Type': 'application/json','Authorization': token})
            self.assertIn('Please enter a valid return date', str(response.data))

      def test_booking_depature_unavalibale_location(self):
            '''test booking to a depature that the flight does not come from'''
            self.register_user()
            result = self.login_user()
            token = json.loads(result.get_data(as_text=True))['Authorization']

            book = {
                "seat_number":1,
                "mpesa_code": "hdjhhjkdsjkkjs",
                "ticket_status": "booked",
                "trip_type": "return",
                "depature": "mogadishu",
                "destination": "kampala",
                "depature_date":"12-04-2019",
                "return_date":"12-04-2019"
              }
            response = self.client.post('/api/book', data=json.dumps(book), headers={'Content-Type': 'application/json','Authorization': token})
            self.assertIn('Depature terminus unavailable', str(response.data))

      def test_booking_destination_unavailable_location(self):
            '''test booking to a destination that the flight does not go to'''
            self.register_user()
            result = self.login_user()
            token = json.loads(result.get_data(as_text=True))['Authorization']

            book = {
                "seat_number":10,
                "mpesa_code": "hdjhhjkdsjkkjs",
                "ticket_status": "booked",
                "trip_type": "return",
                "depature": "kenya",
                "destination": "new york",
                "depature_date":"12-04-2019",
                "return_date":"12-04-2019"
              }
            response = self.client.post('/api/book', data=json.dumps(book), headers={'Content-Type': 'application/json','Authorization': token})
            self.assertIn('Destination terminus unavailable', str(response.data))

      def booking_unavailable_seat(self):
            '''test trying to book a seat that is unavailable/already booked'''
            self.register_user()
            result = self.login_user()
            token = json.loads(result.get_data(as_text=True))['Authorization']

            book = {
                "seat_number":1,
                "mpesa_code": "hdjhhjkdsjkkjs",
                "ticket_status": "booked",
                "trip_type": "return",
                "depature": "kenya",
                "destination": "kampala",
                "depature_date":"12-04-2019",
                "return_date":"12-04-2019"
              }
            response = self.client.post('/api/book', data=json.dumps(book), headers={'Content-Type': 'application/json','Authorization': token})
            self.assertIn('Sorry! That seat has already been booked', str(response.data))

#reserve
      def test_reserve_seat(self):
          '''test reserving a seat'''
          response = self.reserve_a_seat()
          self.assertEqual(response.status_code, 201)

      def test_reserving_missing_destination(self):
          '''test reserving with missing reserving details'''
          self.register_user()
          result = self.login_user()
          token = json.loads(result.get_data(as_text=True))['Authorization']

          reserve = {
                "seat_number":9,
                "ticket_status": "reserved",
                "trip_type": "return",
                "depature": "kenya",
                "depature_date":"12-04-2019",
                "return_date":"12-04-2019"
              }
          response = self.client.get('/api/book', data=reserve, headers={'Content-Type': 'application/json','Authorization': token})
          self.assertIn('Please enter your destination', str(response.data))

      def test_reserving_missing_depature(self):
          '''test reserving with missing reserving details'''
          self.register_user()
          result = self.login_user()
          token = json.loads(result.get_data(as_text=True))['Authorization']

          reserve = {
                "seat_number":5,
                "ticket_status": "reserved",
                "trip_type": "return",
                "destination": "kenya",
                "depature_date":"12-04-2019",
                "return_date":"12-04-2019"
              }
          response = self.client.get('/api/book', data=reserve, headers={'Content-Type': 'application/json','Authorization': token})
          self.assertIn('Please enter your depature', str(response.data))

      def test_reserving_missing_depature_date(self):
          '''test reserving with missing reserving details'''
          self.register_user()
          result = self.login_user()
          token = json.loads(result.get_data(as_text=True))['Authorization']

          reserve = {
                "seat_number":5,
                "ticket_status": "reserved",
                "trip_type": "return",
                "destination": "mombasa",
                "depature": "kampala",
                "return_date":"12-04-2019"
              }
          response = self.client.get('/api/book', data=reserve, headers={'Content-Type': 'application/json','Authorization': token})
          self.assertIn('Please enter your depature date', str(response.data))

      def test_reserving_missing_return_date(self):
          '''test reserving with missing reserving details'''
          self.register_user()
          result = self.login_user()
          token = json.loads(result.get_data(as_text=True))['Authorization']

          reserve = {
                "seat_number":5,
                "ticket_status": "reserved",
                "trip_type": "return",
                "destination": "mombasa",
                "depature": "kampala",
                "return_date":"12-04-2019"
              }
          response = self.client.get('/api/book', data=reserve, headers={'Content-Type': 'application/json','Authorization': token})
          self.assertIn('Please enter your return date', str(response.data))
      def test_reserving_depature_unavalibale_location(self):
            '''test reserving to a depature that the flight does not come from'''
            self.register_user()
            result = self.login_user()
            token = json.loads(result.get_data(as_text=True))['Authorization']

            reserve = {
                "seat_number":2,
                "ticket_status": "reserved",
                "trip_type": "return",
                "depature": "dubai",
                "destination": "kampala",
                "depature_date":"12-04-2019",
                "return_date":"12-04-2019"
              }
            response = self.client.post('/api/book', data=json.dumps(reserve), headers={'Content-Type': 'application/json','Authorization': token})
            self.assertIn('Depature terminus unavailable', str(response.data))


      def test_reserving_destination_unavailable_location(self):
            '''test reserving to a destination that the flight does not go to'''
            self.register_user()
            result = self.login_user()
            token = json.loads(result.get_data(as_text=True))['Authorization']

            reserve = {
                "seat_number":2,
                "ticket_status": "reserved",
                "trip_type": "return",
                "depature": "kenya",
                "destination": "qatar",
                "depature_date":"12-04-2019",
                "return_date":"12-04-2019"
              }
            response = self.client.post('/api/book', data=json.dumps(reserve), headers={'Content-Type': 'application/json','Authorization': token})
            self.assertIn('Destination terminus unavailable', str(response.data))

      def test_reserving_a_past_depature_date(self):
            '''test booking a past date'''
            self.register_user()
            result = self.login_user()
            token = json.loads(result.get_data(as_text=True))['Authorization']

            reserve = {
                "seat_number":2,
                "ticket_status": "reserved",
                "trip_type": "return",
                "depature": "kenya",
                "destination": "kampala",
                "depature_date":"12-04-2017",
                "return_date":"12-04-2019"
              }
            response = self.client.post('/api/book', data=json.dumps(reserve), headers={'Content-Type': 'application/json','Authorization': token})
            self.assertIn('Please enter a valid depature date', str(response.data))

      def test_reserving_a_past_depature_date(self):
            '''test booking a past date'''
            self.register_user()
            result = self.login_user()
            token = json.loads(result.get_data(as_text=True))['Authorization']

            reserve = {
                "seat_number":2,
                "ticket_status": "reserved",
                "trip_type": "return",
                "depature": "kenya",
                "destination": "kampala",
                "depature_date":"12-04-2019",
                "return_date":"12-04-2010"
              }
            response = self.client.post('/api/book', data=json.dumps(reserve), headers={'Content-Type': 'application/json','Authorization': token})
            self.assertIn('Please enter a valid destination date', str(response.data))

      def test_reserving_status_with_mpesa_code(self):
            '''test reserve with mpesa code'''
            self.register_user()
            result = self.login_user()
            token = json.loads(result.get_data(as_text=True))['Authorization']

            reserve = {
                "seat_number":2,
                "mpesa_code": "hdjhhjkdsjkkjs",
                "ticket_status": "reserved",
                "trip_type": "return",
                "depature": "kenya",
                "destination": "kampala",
                "depature_date":"12-04-2019",
                "return_date":"12-04-2019"
              }
            response = self.client.post('/api/book', data=json.dumps(reserve), headers={'Content-Type': 'application/json','Authorization': token})
            self.assertIn('Mpesa code found, Ticket status changed to booked', str(response.data))

      def test_reserving_unavailable_seat(self):
            '''test trying to reserve a seat that is unavailable/already booked'''
            self.register_user()
            result = self.login_user()
            token = json.loads(result.get_data(as_text=True))['Authorization']

            reserve = {
                "seat_number":1,
                "ticket_status": "reserved",
                "trip_type": "return",
                "depature": "kenya",
                "destination": "kampala",
                "depature_date":"12-04-2019",
                "return_date":"12-04-2019"
              }
            response = self.client.post('/api/book', data=json.dumps(reserve), headers={'Content-Type': 'application/json','Authorization': token})
            self.assertIn('Sorry! That seat has already been booked', str(response.data))

#Get_All
      def test_get_all(self):
          self.register_user()
          result = self.login_user()
          token = json.loads(result.get_data(as_text=True))['Authorization']
          response =  self.client.post('/api/get_all', headers={'Content-Type': 'application/json','Authorization': token})
          self.assertIn('WELCOME TO AIRTECH!!!!', str(response.data))

#Get_empty_seats
      def test_get_empty_seats(self):
          self.register_user()
          result = self.login_user()
          token = json.loads(result.get_data(as_text=True))['Authorization']
          destination = {"destination": "mombasa"}
          response =  self.client.post('/api/get_empty_seats', data=json.dumps(destination), headers={'Content-Type': 'application/json','Authorization': token})
          self.assertIn('WELCOME TO AIRTECH!!!!', str(response.data))

      def test_get_empty_seats_no_destination(self):
          self.register_user()
          result = self.login_user()
          token = json.loads(result.get_data(as_text=True))['Authorization']
          destination = {"destination": ""}
          response =  self.client.post('/api/get_empty_seats', data=json.dumps(destination), headers={'Content-Type': 'application/json','Authorization': token})
          self.assertIn('where are you going', str(response.data))

      def test_get_empty_seats_destination_unavailable(self):
          self.register_user()
          result = self.login_user()
          token = json.loads(result.get_data(as_text=True))['Authorization']
          destination = {"destination": "dubai"}
          response =  self.client.post('/api/get_empty_seats', data=json.dumps(destination), headers={'Content-Type': 'application/json','Authorization': token})
          self.assertIn('we may not be going to that destination!', str(response.data))

#Get_reserved_seats
      def test_get_reserved_seats(self):
          self.register_user()
          result = self.login_user()
          token = json.loads(result.get_data(as_text=True))['Authorization']
          flight_details = {"flight_number": "klm-0098", "depature_date":"12-04-2019"}
          response =  self.client.post('/api/get_reserved_seats', data=json.dumps(flight_details), headers={'Content-Type': 'application/json','Authorization': token})
          self.assertIn('something', str(response.data))

      def test_get_reserved_seats_no_flight_number(self):
          self.register_user()
          result = self.login_user()
          token = json.loads(result.get_data(as_text=True))['Authorization']
          flight_details = {"flight_number": "", "depature_date":"12-04-2019"}
          response =  self.client.post('/api/get_reserved_seats', data=json.dumps(flight_details), headers={'Content-Type': 'application/json','Authorization': token})
          self.assertIn('please enter a flight number', str(response.data))
      def test_get_reserved_seats_no_depature_date(self):
          self.register_user()
          result = self.login_user()
          token = json.loads(result.get_data(as_text=True))['Authorization']
          flight_details = {"flight_number": "klm-0098", "depature_date":""}
          response =  self.client.post('/api/get_reserved_seats', data=json.dumps(flight_details), headers={'Content-Type': 'application/json','Authorization': token})
          self.assertIn('please enter a date', str(response.data))


def tearDown(self):
    """teardown all initialized variables."""
    with self.app.app_context():
        # drop all tables
        db.session.remove()
        db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
