import time
import random
from locust import between, task, FastHttpUser

class WagonFakeUser(FastHttpUser):
    pass  # YOUR CODE HERE