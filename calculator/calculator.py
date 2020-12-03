import string
from functools import reduce


class CustomError:
    def __init__(self, message):
        self.message = message

    def display(self):
        if self.message:
            print(self.message)
        else:
            pass


class Memory:
    def __init__(self):
        self.memory = {}

    def get(self, key):
        try:
            return int(self.memory.get(key))
        except (TypeError, ValueError):
            reference_value = self.memory.get(key)
            if reference_value:
                return self.get(reference_value)
            return None

    def update(self, args):
        self.memory.update(args)

    def __repr__(self):
        for key, value in self.memory.items():
            return f"Memory -- {key}: {value}"


class Command:
    """A basic list of command as methods"""

    def __init__(self, instruction):
        self.instruction = instruction

    @staticmethod
    def help():
        print(
            f"""
                A smart calculator that evaluates results based on inputs, possible inputs:
                - Integer value (positive or negative)
                - Equation
                    - Sum
                    - Subtract
                - Variable 
                    - Variable Assignment
                    - Variable Equation (Sum and Substract)
                - /help
                - /exit

                Validation is included for a non operator and non digit
            """
        )

    @staticmethod
    def error():
        print("Unknown command")

    @staticmethod
    def exit():
        print("Bye!")
        exit()

    def __repr__(self):
        return f"Command {self.instruction}"


class CommandCenter:
    """Execute commands based on parsed result"""

    def __init__(self, command):
        self.command = command

    def execute(self):
        if self.command:
            try:
                getattr(self.command, self.command.instruction)()
            except AttributeError:
                self.command.error()
        else:
            pass


class Parser:
    """A parser for user inputs will be used as programs entrypoint"""

    def __init__(self, contents):
        self.contents = contents
        self.__commands = None
        self.__parsed = []

    def parse(self):
        temp = [Operator("+")]

        for index, content in enumerate(self.contents):
            if self.is_operand(content):
                temp.append(Digit(content))
                if len(temp) == 3 or index == len(self.contents) - 1:
                    self.__parsed.append(temp if len(temp) == 3 else temp + [Digit(0)])
                    temp = []

            elif self.is_operator(content):
                if temp and isinstance(temp[0], Operator):
                    self.__parsed.append(temp if len(temp) == 3 else temp + [Digit(0)])
                    temp = [Operator(content)]
                else:
                    temp.insert(0, Operator(content))

    def get_command(self):
        return self.__commands

    def get_parsed(self):
        return self.__parsed

    @staticmethod
    def is_operand(content):
        try:
            int(content)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_operator(content):
        if content.count("+") == len(content):
            return True

        elif content.count("-") == len(content):
            return True

        else:
            return False


class Digit:
    """A representation of digit"""

    def __init__(self, number):
        self.number = int(number)

    def __repr__(self):
        return f"Digit {self.number}"

    def __str__(self):
        return f"{self.number}"


class Operator:
    """A representation of operator"""

    def __init__(self, op):
        self.operator = self.determine_operator_method(op)

    def __repr__(self):
        return f"Operator {self.operator}"

    @staticmethod
    def determine_operator_method(op):
        if op.count("-") % 2 == 1:
            return "subtract"
        else:
            return "add"

    @staticmethod
    def add(*operands):
        return reduce(lambda a, b: a + b, operands)

    @staticmethod
    def subtract(*operands):
        return reduce(lambda a, b: a - b, operands)


class Variable:
    """A representation of variable"""

    def __init__(self, variable):
        self.variable = variable

    def __repr__(self):
        return f"Variable {self.variable}"

    @staticmethod
    def is_valid(variable):
        alphabet = string.ascii_letters
        count = 0
        for k in variable:
            count += alphabet.count(k)

        return count == len(variable)


class Calculator:
    """A Calculator for parsed mathematical equation based on operand and operator"""

    def __init__(self, parsed):
        self.parsed = parsed
        self.result = None

    def calculate(self):
        temp = []

        for (operator, first_operand, second_operand) in self.parsed:
            if not second_operand.number:
                result = getattr(operator, operator.operator)(second_operand.number, first_operand.number)
                temp.append(result)
            else:
                result = getattr(operator, operator.operator)(first_operand.number, second_operand.number)
                temp.append(result)

        if len(temp):
            self.result = sum(temp)

    def print(self):
        if isinstance(self.result, int):
            print(self.result)


class Validator:
    def __init__(self, content, memory):
        self.content = content
        self.memory = memory

    def validate(self):
        if not self.content:
            return self.format(error=CustomError(message=None))

        if self.content.startswith("/"):
            return self.format(success=Command(instruction=self.content.split("/")[1]))

        if self.is_assignment(content=self.content):
            key = self.extract_key(self.content)
            value = self.extract_value(self.content)

            if not Variable.is_valid(key):
                return self.format(error=CustomError(message="Invalid identifier"))

            if not Validator.is_valid_assignee(value):
                return self.format(error=CustomError(message="Invalid assignment"))

            if not self.is_in_memory(value):
                return self.format(error=CustomError(message="Unknown variable"))

            return self.format(success=({key: value}))

        if Variable.is_valid(variable=self.content) and not self.is_in_memory(content=self.content):
            return self.format(error=CustomError(message="Unknown variable"))

        else:
            return self.format(success=Translator(equation=self.content))

    @staticmethod
    def format(success=None, error=None):
        return success, error

    def is_in_memory(self, content):
        try:
            return type(int(content)) == int
        except ValueError:
            return type(self.memory.get(content)) == int

    @staticmethod
    def is_valid_assignee(content):
        try:
            return Variable.is_valid(variable=content) or type(int(content)) == int
        except (TypeError, ValueError):
            return False

    @staticmethod
    def is_assignment(content):
        return content.count("=")

    @staticmethod
    def extract_key(contents):
        key, *_ = [x.strip() for x in contents.split("=") if x.strip()]
        return key

    @staticmethod
    def extract_value(contents):
        try:
            _, value = [x.strip() for x in contents.split("=") if x.strip()]
            return value
        except ValueError:
            return None


class Translator:
    def __init__(self, equation):
        self.equation = equation

    def translate(self, memory):
        return [memory.get(val) if Variable.is_valid(val) else val for val in self.equation.split()]

    @staticmethod
    def format(success=None, error=None):
        return success, error


def main():
    memory = Memory()
    while True:
        user_input = input()

        success, error = Validator(user_input, memory).validate()

        if isinstance(error, CustomError):
            error.display()
            continue

        if isinstance(success, Command):
            command_center = CommandCenter(command=success)
            command_center.execute()

        if isinstance(success, dict):
            memory.update(success)

        if isinstance(success, Translator):
            content = success.translate(memory=memory)

            parser = Parser(contents=content)
            parser.parse()

            calculator = Calculator(parsed=parser.get_parsed())
            calculator.calculate()
            calculator.print()


main()
