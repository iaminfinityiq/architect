class NodeType:
    def __init__(self, type):
        self.type = type

class Statement:
    def __init__(self, type):
        self.type = type

class Program(Statement):
    def __init__(self, body):
        super().__init__(NodeType("Program"))
        self.body = body
    
    def __repr__(self):
        return f"(PROGRAM STATEMENT [\n\t{';\n\t'.join([statement.__repr__() for statement in self.body])}\n])"

class Expression(Statement):
    def __init__(self, type):
        super().__init__(type)

class BinaryExpression(Expression):
    def __init__(self, left, operator, right):
        super().__init__(NodeType("BinaryExpression"))
        self.left = left
        self.operator = operator
        self.right = right
    
    def __repr__(self):
        return f"(BINARY EXPRESSION {self.left} {self.operator} {self.right})"

class UnaryExpression(Expression):
    def __init__(self, sign, value):
        super().__init__(NodeType("UnaryExpression"))
        self.sign = sign
        self.value = value
    
    def __repr__(self):
        return f"(UNARY EXPRESSION {self.sign}{self.value})"

class NumberLiteral(Expression):
    def __init__(self, value):
        super().__init__(NodeType("NumberLiteral"))
        self.value = value
    
    def __repr__(self):
        return f"(NUMBER LITERAL {self.value})"

class BooleanLiteral(Expression):
    def __init__(self, value):
        super().__init__(NodeType("BooleanLiteral"))
        self.value = value
    
    def __repr__(self):
        return f"(BOOLEAN LITERAL {self.value})"

class TrueLiteral(BooleanLiteral):
    def __init__(self):
        super().__init__("true")
    
class FalseLiteral(BooleanLiteral):
    def __init__(self):
        super().__init__("false")

class NullLiteral(Expression):
    def __init__(self):
        super().__init__(NodeType("NullLiteral"))
    
    def __repr__(self) -> str:
        return "(NULL LITERAL)"

class Identifier(Expression):
    def __init__(self, var_name):
        super().__init__(NodeType("Identifier"))
        self.var_name = var_name
    
    def __repr__(self):
        return f"(IDENTIFIER {self.var_name})"

class AssignmentStatement(Statement):
    def __init__(self, var_name, value):
        super().__init__(NodeType("AssignmentStatement"))
        self.var_name = var_name
        self.value = value

    def __repr__(self):
        return f"(ASSIGNMENT STATEMENT: {self.var_name} assigned with {self.value})"

class UpdateStatement(Statement):
    def __init__(self, var_name, value):
        super().__init__(NodeType("UpdateStatement"))
        self.var_name = var_name
        self.value = value
    
    def __repr__(self):
        return f"(UPDATE STATEMENT: {self.var_name} updated with {self.value})"
