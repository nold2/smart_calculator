import re

from commands import Command
from exceptions import CustomError
from operators import OPERATORS
from tokens import Tokenizer
from variables import Variable


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

        if self.is_valid_operator_repetition(content=self.content):
            return self.format(error=CustomError(message="Invalid Expression"))

        if self.is_operator_placement_valid(content=self.content):
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
    def is_valid_operator_repetition(content):
        multiple_multiplication = re.search(r"(\*)\1+", content)
        multiple_division = re.search(r"(/)\1+", content)
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

    @staticmethod
    def is_operator_placement_valid(content):
        startswith = any([content.startswith(op) for op in OPERATORS])
        endswith = any([content.endswith(op) for op in OPERATORS])

        return any([startswith, endswith])
