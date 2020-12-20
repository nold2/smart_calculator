class CustomError:
    """A representation of errors"""

    def __init__(self, message):
        self.message = message

    def display(self):
        if self.message:
            print(self.message)
        else:
            pass