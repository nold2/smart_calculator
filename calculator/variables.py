import string


class Variable:
    """A representation of variable"""

    def __init__(self, variable):
        self.variable = variable

    def __repr__(self):
        return f"Variable {self.variable}"

    @staticmethod
    def is_check(variable):
        alphabet = string.ascii_letters
        count = 0
        for k in variable:
            count += alphabet.count(k)

        return count == len(variable)
