from ..errors import SyntaxError, RuntimeResult

DIGITS = "0123456789"
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"

class TokenType:
    def __init__(self, type):
        self.type = type
    
    def __repr__(self):
        return f"(TOKEN TYPE {self.type})"

class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
    
    def __repr__(self):
        return f"(TOKEN {self.type.__repr__()}{f' with value {self.value}'})"

KEYWORDS = {
    "build": TokenType("Build"),
    "frame": TokenType("Frame"),
    "fix": TokenType("Fix"),
    "with": TokenType("With"),
    "screw": TokenType("Screw"),
    "true": TokenType("True"),
    "false": TokenType("False"),
    "null": TokenType("Null"),
    "decision": TokenType("Decision"),
    "if": TokenType("If"),
    "else": TokenType("Else")
}

def tokenize(text):
    src = list(text)
    tokens = []
    while src:
        match src[0]:
            case "$":
                # repeat until the newline
                while src[0] != "\n":
                    src.pop(0)
                    if not src:
                        return RuntimeResult(tokens + [Token(TokenType("EOF"))], None)
            case "+":
                tokens += [Token(TokenType("Plus"), src.pop(0))]
            case "-":
                tokens += [Token(TokenType("Minus"), src.pop(0))]
            case "*":
                tokens += [Token(TokenType("Multiply"), src.pop(0))]
            case "/":
                tokens += [Token(TokenType("Divide"), src.pop(0))]
            case "^":
                tokens += [Token(TokenType("Power"), src.pop(0))]
            case "(":
                tokens += [Token(TokenType("OpenParen"), src.pop(0))]
            case ")":
                tokens += [Token(TokenType("CloseParen"), src.pop(0))]
            case "\n":
                tokens += [Token(TokenType("Newline"), src.pop(0))]
            case _:
                if src[0] in "\t ":
                    src.pop(0)
                    continue

                if src[0] in DIGITS:
                    number = ""
                    while src[0] in DIGITS:
                        number += src.pop(0)
                        if not src:
                            break
                    
                    count = number.count(".")
                    if count > 1:
                        return RuntimeResult(None, SyntaxError(f"Expected 0 or 1 '.' in a number, got {count}/1"))
                    
                    tokens += [Token(TokenType("Number"), number)]
                    continue
                
                if src[0] in LETTERS:
                    identifier = ""
                    while src[0] in LETTERS + DIGITS:
                        identifier += src.pop(0)
                        if not src:
                            break
                    
                    if identifier in KEYWORDS:
                        tokens += [Token(KEYWORDS[identifier], identifier)]
                        continue

                    tokens += [Token(TokenType("Identifier"), identifier)]
                    continue

                return RuntimeResult(None, SyntaxError(f"Unexpected character: '{src[0]}'"))
    
    return RuntimeResult(tokens + [Token(TokenType("EOF"))], None)