from collections import deque

from commands import Command, CommandCenter
from digits import Digit
from exceptions import CustomError
from memories import Memory
from operators import Precedence, LeftBracket, RightBracket
from tokens import Tokenizer
from validators import Validator


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

    def remove_operator_from_stack(self, operator):
        second_operand = self.__result.pop()
        first_operand = self.__result.pop()
        result = operator.execute(first_operand, second_operand)
        self.__result.append(result)

    def calculate(self):
        for v in self.buffer:
            if isinstance(v, Digit):
                self.__result.append(v.number)
            elif v == LeftBracket:
                self.__operators.append(v)
            elif v == RightBracket:
                operator = self.__operators.pop()

                while not operator == LeftBracket:
                    self.remove_operator_from_stack(operator=operator)

                    operator = self.__operators.pop()
            else:
                while len(self.__operators) and Precedence.lte(v, self.peek(self.__operators)):
                    operator = self.__operators.pop()
                    self.remove_operator_from_stack(operator=operator)

                self.__operators.append(v)

        while len(self.__operators):
            operator = self.__operators.pop()
            self.remove_operator_from_stack(operator=operator)

        return self.__result.pop()


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
