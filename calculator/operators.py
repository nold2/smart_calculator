from functools import reduce

OPERATOR = {
    "-",
    "+",
    "*",
    "^",
    "/",
    ")",
    "("
}


class Operator:
    """A representation of operator"""

    def __init__(self, op):
        self.operator = self.determine_operator_method(op)

    def __repr__(self):
        return f"Operator {self.operator}"

    @staticmethod
    def is_check(op):
        return op in OPERATOR

    @staticmethod
    def determine_operator_method(op):
        if op == "(":
            return LeftBracket

        if op == ")":
            return RightBracket

        if op == "*":
            return Multiplication

        if op == "/":
            return Division

        if op == "^":
            return Exponentiation

        if op.count("-") % 2 == 1:
            return Subtraction

        else:
            return Addition


class Addition:
    def __repr__(self):
        return f"Addition"

    def __hash__(self):
        return hash("+")

    @staticmethod
    def execute(*operands):
        return reduce(lambda a, b: a + b, operands)


class Subtraction:
    def __repr__(self):
        return f"Subtraction"

    def __hash__(self):
        return hash("-")

    @staticmethod
    def execute(*operands):
        return reduce(lambda a, b: a - b, operands)


class Multiplication:
    def __repr__(self):
        return f"Multiplication"

    def __hash__(self):
        return hash("*")

    @staticmethod
    def execute(*operands):
        return reduce(lambda a, b: a * b, operands)


class Division:
    def __repr__(self):
        return f"Division"

    def __hash__(self):
        return hash("/")

    @staticmethod
    def execute(*operands):
        return reduce(lambda a, b: a // b, operands)


class Exponentiation:
    def __repr__(self):
        return f"Exponentiation"

    def __hash__(self):
        return hash("^")

    @staticmethod
    def execute(*operands):
        return reduce(lambda a, b: a ^ b, operands)


class LeftBracket:
    def __hash__(self):
        return hash(")")

    def __repr__(self):
        return "Left Bracket"


class RightBracket:
    def __hash__(self):
        return hash("(")

    def __repr__(self):
        return "Right Bracket"


class Precedence:
    LEVEL = {
        Exponentiation: 2,
        Multiplication: 1,
        Division: 1,
        Addition: 0,
        Subtraction: 0,
        RightBracket: -1,
        LeftBracket: -1,
    }

    @staticmethod
    def lte(*operators):
        op1, op2 = operators
        return Precedence.LEVEL.get(op1) <= Precedence.LEVEL.get(op2)
