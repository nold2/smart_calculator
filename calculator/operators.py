from functools import reduce


class Operator:
    """A representation of operator"""
    OPERATOR = {
        "-",
        "+",
        "*",
        "^",
        "/"
    }

    def __init__(self, op):
        self.operator = self.determine_operator_method(op)

    def __repr__(self):
        return f"Operator {self.operator}"

    @staticmethod
    def is_check(op):
        return op in Operator.OPERATOR

    @staticmethod
    def determine_operator_method(op):
        if op.count("-") % 2 == 1:
            return "subtract"
        if op.count("*") == len(op):
            return "multiply"
        if op.count("/") == len(op):
            return "divide"
        else:
            return "add"

    @staticmethod
    def add(*operands):
        return reduce(lambda a, b: a + b, operands)

    @staticmethod
    def subtract(*operands):
        return reduce(lambda a, b: a - b, operands)

    @staticmethod
    def multiply(*operands):
        return reduce(lambda a, b: a * b, operands)

    @staticmethod
    def divide(*operands):
        return reduce(lambda a, b: a / b, operands)
