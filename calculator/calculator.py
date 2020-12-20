import re
from collections import deque

from commands import Command, CommandCenter
from digits import Digit
from exceptions import CustomError
from memories import Memory
from operators import Operator, Precedence, LeftBracket, RightBracket
from variables import Variable


class Calculator:
    """A Calculator for parsed mathematical equation based on operand and operator"""

    def __init__(self, buffer):
        self.buffer = buffer
        self.__commands = None
        self.__result = deque()
        self.__operators = deque()

    @staticmethod
    def peek(queue):
        return queue[-1]

    def calculate(self):
        for v in self.buffer:
            if isinstance(v, Digit):
                self.__result.append(v.number)
            elif v == LeftBracket:
                self.__operators.append(v)
            elif v == RightBracket:
                operator = self.__operators.pop()

                while not operator == LeftBracket:
                    second_operand = self.__result.pop()
                    first_operand = self.__result.pop()

                    result = operator.execute(first_operand, second_operand)
                    self.__result.append(result)

                    operator = self.__operators.pop()
            else:
                while len(self.__operators) and Precedence.lte(v, self.peek(self.__operators)):
                    operator = self.__operators.pop()
                    second_operand = self.__result.pop()
                    first_operand = self.__result.pop()

                    result = operator.execute(first_operand, second_operand)
                    self.__result.append(result)

                self.__operators.append(v)

        while len(self.__operators):
            operator = self.__operators.pop()
            second_operand = self.__result.pop()
            first_operand = self.__result.pop()
            result = operator.execute(first_operand, second_operand)
            self.__result.append(result)

        return self.__result.pop()


class Tokenizer:
    def __init__(self, buffer, memory):
        self.buffer = buffer
        self.memory = memory
        self.pos = 0
        self.tokens = deque()

    def __next_token(self):
        atom = self.__get_atom()
        while atom and atom.isspace():
            self.pos += 1
            atom = self.__get_atom()

        if atom is None:
            return None

        if Digit.is_check(atom):
            return self.__tokenize(Digit)

        if Operator.is_check(atom):
            return self.__tokenize(Operator).operator

        if Variable.is_check(atom):
            var = self.__tokenize(Variable).variable
            digit = self.memory.get(var)
            return Digit(digit)

    def __tokenize(self, meta):
        end_pos = self.pos + 1
        while self.__get_atom(end_pos) and meta.is_check(self.__get_atom(end_pos)):
            end_pos += 1

        value = self.buffer[self.pos:end_pos]
        self.pos = end_pos

        return meta(value)

    def __get_atom(self, pos=None):
        current_pos = pos or self.pos

        try:
            return self.buffer[current_pos]
        except IndexError:
            return None

    def tokenize(self):
        while True:
            token = self.__next_token()

            if not token:
                break
            else:
                self.tokens.append(token)

        return self.tokens


class Validator:
    """Validates user input before any actions occur"""

    def __init__(self, content, memory):
        self.content = content
        self.memory = memory

    def validate(self):
        if not self.content:
            return self.format(error=CustomError(message=None))

        if self.is_command(content=self.content):
            return self.format(success=Command(instruction=self.content.split("/")[1]))

        if self.is_assignment(content=self.content):
            key = self.extract_key(self.content)
            value = self.extract_value(self.content)

            if not Variable.is_check(key):
                return self.format(error=CustomError(message="Invalid identifier"))

            if not Validator.is_valid_assignee(value):
                return self.format(error=CustomError(message="Invalid assignment"))

            if not self.is_in_memory(value):
                return self.format(error=CustomError(message="Unknown variable"))

            return self.format(success=({key: value}))

        if self.is_variable_valid_and_exists(content=self.content):
            return self.format(error=CustomError(message="Unknown variable"))

        if self.is_valid_single_character(content=self.content):
            return self.format(error=CustomError(message="Unknown variable"))

        if self.is_open_and_close_bracket_balance(content=self.content):
            return self.format(error=CustomError(message="Invalid Expression"))

        if self.is_valid_operator(content=self.content):
            return self.format(error=CustomError(message="Invalid Expression"))

        else:
            return self.format(success=Tokenizer(buffer=self.content, memory=self.memory))

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
            return Variable.is_check(variable=content) or type(int(content)) == int
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

    @staticmethod
    def is_valid_operator(content):
        multiple_multiplication = re.search(r"(\*)\1+", content)
        multiple_division = re.search(r"(\/)\1+", content)
        multiple_Exponentiation = re.search(r"(\^)\1+", content)

        return any([multiple_multiplication, multiple_division, multiple_Exponentiation])

    @staticmethod
    def is_open_and_close_bracket_balance(content):
        return not content.count("(") == content.count(")")

    def is_valid_single_character(self, content):
        return len(content.split()) == 1 and not self.is_valid_assignee(content=content)

    @staticmethod
    def is_command(content):
        return content.startswith("/")

    def is_variable_valid_and_exists(self, content):
        return Variable.is_check(variable=content) and not self.is_in_memory(content=content)


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

        if isinstance(success, Tokenizer):
            parsed_tokens = success.tokenize()

            calculator = Calculator(buffer=parsed_tokens)
            result = calculator.calculate()
            print(result)


main()
