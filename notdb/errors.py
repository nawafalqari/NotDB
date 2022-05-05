class InvalidHostError(Exception):
    def __init__(self, element, message="Invalid host"):
        self.element = element
        self.message = message

        super().__init__(self.message)
    def __str__(self):
        return f'"{self.element}": {self.message}'

class WrongPasswordError(Exception):
    def __init__(self, message="Password is wrong"):
        self.message = message

        super().__init__(self.message)

class InvalidDictError(Exception):
    def __init__(self, element, message='Invalid "SET" update must have only one key'):
        self.element = element
        self.message = message

        super().__init__(self.message)
    def __str__(self):
        return f'"{self.element}": {self.message}'