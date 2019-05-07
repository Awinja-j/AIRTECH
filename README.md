# AIRTECH API

This is a flight booking system that allows you to:
- Login/Logout
- Upload password photo
- Book tickets
- Recieve tickets as email
- Check the status of your flight
- Make flight reservations
- Purchase tickets

# The building blocks used are:

- python version 3.6
- Flask
- PostgresSQL

# Installation
The following set of steps are necessary to facilitate running the application locally:

1. clone the following repo https://github.com/Awinja-Andela/AIRTECH.git

2. cd into Bucketlist-Server and create a VirtualEnvironment using the following command: virtualenv <name_of_env>

3. To activate the virtualenv, cd into the <name_of_env>/bin/ and use the following command: source activate

4. To install all app requirements pip install -r requirements.txt

5. Create the database and run migrations

        $ python manage.py db init

        $ python manage.py db migrate

        $ python manage.py db upgrade

You are now set! you can now run the server using `python manage.py runserver` command

Interact with the API, send http requests using Postman


| URL ENDPOINT          | HTTP METHODS | SUMMARY                                                             |
|-----------------------|--------------|---------------------------------------------------------------------|
| /auth/register        | POST         | register user and upload user passport photo                        |
| /auth/upload_passport | POST         | upload passport photo if not done during registration               |
| /auth/login           | POST         | login to the api                                                    |
| /auth/logout          | POST         | logout of the api                                                   |
| /api/get_empty_seats        | GET          | Get a list of empty seats in the flight                       |
| /api/book      | POST         | book/reserve a ticket |
| /api/get_reserved_seats     | GET         | get a list of all seats that have been reserved                                        |
| /          | GET         | Index/ Welcome page                         |

To run the load tester, use the following commands:

locust -H https://`server_name` -f locust.py

Then load the Locust.io user interface in a web browser. Just point to the hostname/IP on port 8089.

`https://<server_name>:8089`
