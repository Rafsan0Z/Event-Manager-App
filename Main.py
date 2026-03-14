from EmailHandler import EmailFactory

class Main:

    def __init__(self):
        self.handler = EmailFactory()

test = Main()
test.handler.get_labels()