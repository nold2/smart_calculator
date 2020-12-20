from digits import Digit
from operators import Operator
from variables import Variable


class Tokenizer:
    """Tokenize a complex equation into a list of Digits and Operators exclusively"""

    def __init__(self, buffer, memory):
        self.buffer = buffer
        self.memory = memory
        self.pos = 0
        self.tokens = []

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
