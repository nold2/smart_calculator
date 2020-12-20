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
