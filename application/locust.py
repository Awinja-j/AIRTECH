from locust import HttpLocust, TaskSet

def register(l):
      l.client.post("/auth/register", {"name": "jojo bear", "email":"jojo@email.com", "password": "password1234", "passport":"www.url.com"})

def login(l):
    l.client.post("/auth/login", {"email":"jojo@email.com", "password": "password1234",})

def logout(l):
    l.client.post("/auth/logout", {"email":"jojo@email.com", "password": "password1234",})

def index(l):
    l.client.get("/api")

def book_ticket(l):
    l.client.get("/api/book_ticket")

def get_reserved_seats(l):
    l.client.get("/api/get_reserved_seats")

def get_all(l):
    l.client.get("/api/get_all")

def get_empty_seats(l):
    l.client.get("/api/get_empty_seats")

class UserBehavior(TaskSet):
    tasks = {index: 2, get_all: 1}

    def on_start(self):
        login(self)

    def on_stop(self):
        logout(self)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
