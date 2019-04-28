from locust import HttpLocust, TaskSet

def register(l):
      l.client.post("/auth/register", {"name": "jojo bear", "email":"jojo@email.com", "password": "password1234", "passport":"www.url.com"})

def login(l):
    l.client.post("/auth/login", {"email":"jojo@email.com", "password": "password1234",})

def logout(l):
    l.client.post("/auth/logout", {"email":"jojo@email.com", "password": "password1234",})

def index(l):
    l.client.get("/")

def profile(l):
    l.client.get("/auth/profile")

class UserBehavior(TaskSet):
    tasks = {index: 2, profile: 1}

    def on_start(self):
        login(self)

    def on_stop(self):
        logout(self)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
