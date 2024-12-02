import sys

# Base class
class ErrorType:
    def __init__(self, type):
        self.type = type

class Error:
    def __init__(self, error, reason, error_code):
        self.error = error
        self.reason = reason
        self.error_code = error_code
    
    def show_error(self):
        sys.stdout.write(f"{self.error.type}: {self.reason}")
        sys.exit(self.error_code)

class RuntimeResult:
    def __init__(self, result, error):
        self.result = result
        self.error = error

# Errors
class SyntaxError(Error):
    def __init__(self, reason):
        super().__init__(ErrorType("SyntaxError"), reason, 1)

class VariableError(Error):
    def __init__(self, reason):
        super().__init__(ErrorType("VariableError"), reason, 2)

class MathError(Error):
    def __init__(self, reason):
        super().__init__(ErrorType("MathError"), reason, 3)

class DataTypeError(Error):
    def __init__(self, reason):
        super().__init__(ErrorType("DataTypeError"), reason, 4)

# Development errors
class InterpreterError(Error):
    def __init__(self, reason):
        super().__init__(ErrorType("InterpreterError"), reason)