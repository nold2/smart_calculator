class Memory:
    """A representation of memory to store variables as key along with their values"""

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
