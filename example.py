
from my_selenium import MySelenium

class Example(MySelenium):
    def __init__(self, user_id, password):
        super().__init__()
        self.user_id = user_id
        self.password = password

    def login(self):
        pass

    