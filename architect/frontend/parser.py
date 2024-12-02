from .abstract_syntax_tree import *
from ..errors import RuntimeResult, SyntaxError

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
    
    def at(self):
        return self.tokens[0]

    def eat(self):
        return self.tokens.pop(0)
    
    def expect(self, *expected, error):
        token = self.tokens.pop(0)
        if token.type.type not in expected:
            if self.in_end(token):
                return RuntimeResult(None, error)
            
            return RuntimeResult(None, SyntaxError(f"{error.reason}, got '{token.value}'"))
        
        return RuntimeResult(token, None)

    def in_end(self, token):
        return token.type.type in ("EOF", "Newline")

    def not_eof(self):
        return self.at().type.type != "EOF"

    def produce_ast(self):
        program = Program([])
        while self.not_eof():
            rt = self.parse_statement()
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            program.body += [rt.result]
            while self.at().type.type == "Newline":
                self.eat()

        return RuntimeResult(program, None)

    def parse_statement(self):
        match self.at().type.type:
            case "Build":
                self.eat()

                # choose type to build
                rt = self.expect("Frame", error=SyntaxError("Expected 'frame'"))
                if rt.error:
                    return RuntimeResult(None, rt.error)
                
                match rt.result.type.type:
                    case "Frame":
                        # variable
                        rt = self.parse_build_frame_statement()
                        if rt.error:
                            return RuntimeResult(None, rt.error)
                        
                        return RuntimeResult(rt.result, None)
            case "Fix":
                self.eat()
                rt = self.expect("Frame", error=SyntaxError("Expected 'frame'"))
                if rt.error:
                    return RuntimeResult(None, rt.error)
                
                match rt.result.type.type:
                    case "Frame":
                        rt = self.parse_fix_frame_statement()
                        if rt.error:
                            return RuntimeResult(None, rt.error)
                        
                        return RuntimeResult(rt.result, None)
            case "Decision":
                rt = self.parse_if_statement()
                if rt.error:
                    return RuntimeResult(None, rt.error)
                
                return RuntimeResult(rt.result, None)
            case _:
                rt = self.parse_expression()
                if rt.error:
                    return RuntimeResult(None, rt.error)
                
                return RuntimeResult(rt.result, None)
    
    def parse_build_frame_statement(self):
        rt = self.expect("Identifier", error=SyntaxError("Expected identifier"))
        identifier = rt.result.value

        rt = self.expect("With", error=SyntaxError("Expected 'with'"))
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        rt = self.expect("Screw", error=SyntaxError("Expected 'screw'"))
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        rt = self.parse_expression()
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        if not self.in_end(self.at()):
            return RuntimeResult(None, SyntaxError(f"Expected newline, got '{self.at().type.type}'"))
        
        return RuntimeResult(AssignmentStatement(identifier, rt.result), None)

    def parse_fix_frame_statement(self):
        rt = self.expect("Identifier", error=SyntaxError("Expected identifier"))
        identifier = rt.result.value

        rt = self.expect("With", error=SyntaxError("Expected 'with'"))
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        rt = self.expect("Screw", error=SyntaxError("Expected 'screw'"))
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        rt = self.parse_expression()
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        if not self.in_end(self.at()):
            return RuntimeResult(None, SyntaxError(f"Expected newline, got '{self.at().type.type}'"))

        return RuntimeResult(UpdateStatement(identifier, rt.result), None)

    def parse_if_statement(self):
        self.eat()
        

    def parse_expression(self):
        rt = self.parse_additive_expression()
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        return RuntimeResult(rt.result, None)
    
    def parse_additive_expression(self):
        left = self.parse_multiplicative_expression()
        if left.error:
            return RuntimeResult(None, left.error)
        
        left = left.result
        while self.at().type.type in ("Plus", "Minus"):
            operator = self.eat()
            right = self.parse_multiplicative_expression()
            if right.error:
                return RuntimeResult(None, right.error)
            
            left = BinaryExpression(left, operator.type.type, right.result)
        
        return RuntimeResult(left, None)
    
    def parse_multiplicative_expression(self):
        left = self.parse_exponentation_expression()
        if left.error:
            return RuntimeResult(None, left.error)
        
        left = left.result
        while self.at().type.type in ("Multiply", "Divide"):
            operator = self.eat()
            right = self.parse_exponentation_expression()
            if right.error:
                return RuntimeResult(None, right.error)
            
            left = BinaryExpression(left, operator.type.type, right.result)
        
        return RuntimeResult(left, None)
    
    def parse_exponentation_expression(self):
        rt = self.parse_unary_expression()
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        elements = [rt.result]
        while self.at().type.type == "Power":
            self.eat()
            rt = self.parse_unary_expression()
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            elements += [rt.result]
        
        elements = elements[::-1]
        left = None
        for element in elements:
            if left:
                left = BinaryExpression(element, "Power", left)
            else:
                left = element
        
        return RuntimeResult(left, None)

    def parse_unary_expression(self):
        if self.at().type.type not in ("Plus", "Minus"):
            rt = self.parse_primary_expression()
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(rt.result, None)
        
        sign = "+"
        while self.at().type.type in ("Plus", "Minus"):
            operator = self.eat()
            if operator.type.type == "Minus":
                sign = "-" if sign == "+" else "-"
        
        rt = self.parse_primary_expression()
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        return RuntimeResult(UnaryExpression(sign, rt.result), None)
    
    def parse_primary_expression(self):
        match self.at().type.type:
            case "Identifier":
                return RuntimeResult(Identifier(self.eat().value), None)
            case "Number":
                return RuntimeResult(NumberLiteral(float(self.eat().value)), None)
            case "True":
                self.eat()
                return RuntimeResult(TrueLiteral(), None)
            case "False":
                self.eat()
                return RuntimeResult(FalseLiteral(), None)
            case "Null":
                self.eat()
                return RuntimeResult(NullLiteral(), None)
            case "OpenParen":
                self.eat()
                expression = self.parse_expression()
                if expression.error:
                    return RuntimeResult(None, expression.error)
                
                rt = self.expect("CloseParen", error=SyntaxError("Expected ')'"))
                if rt.error:
                    return RuntimeResult(None, rt.error)
                
                return RuntimeResult(expression.result, None)
            case _:
                return RuntimeResult(None, SyntaxError(f"Unexpected token found: '{self.at()}'"))