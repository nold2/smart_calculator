class Digit:
    """A representation of digit"""

    def __init__(self, number):
        self.number = int(number)

    def __repr__(self):
        return f"Digit {self.number}"

    def __str__(self):
        return f"{self.number}"

    @staticmethod
    def is_check(value):
        return value.isdigit()