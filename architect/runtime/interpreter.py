from ..errors import RuntimeResult, MathError, InterpreterError, DataTypeError
from .values import *

def evaluate_program(ast_node, environment):
    last_evaluated = None
    for statement in ast_node.body:
        rt = evaluate(statement, environment)
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        last_evaluated = rt.result
    
    return RuntimeResult(last_evaluated, None)

def evaluate(ast_node, environment):
    match ast_node.type.type:
        case "Program":
            rt = evaluate_program(ast_node, environment)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(rt.result, None)
        case "Identifier":
            rt = evaluate_identifier(ast_node, environment)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(rt.result, None)
        case "NumberLiteral":
            rt = evaluate_number_literal(ast_node)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(rt.result, None)
        case "BooleanLiteral":
            return RuntimeResult(Boolean(ast_node.value), None)
        case "NullLiteral":
            return RuntimeResult(Null(), None)
        case "UnaryExpression":
            rt = evaluate_unary_expression(ast_node, environment)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(rt.result, None)
        case "BinaryExpression":
            rt = evaluate_binary_expression(ast_node, environment)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(rt.result, None)
        case "AssignmentStatement":
            rt = evaluate_variable_assignment(ast_node, environment)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(rt.result, None)
        case "UpdateStatement":
            rt = evaluate_variable_update(ast_node, environment)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(rt.result, None)
        case _:
            return RuntimeResult(None, InterpreterError(f"This AST node has not been setup for interpretion yet: {ast_node}"))
    
def evaluate_identifier(ast_node, environment):
    rt = environment.lookup(ast_node.var_name)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    return RuntimeResult(rt.result, None)

def evaluate_number_literal(ast_node):
    return RuntimeResult(create_number(ast_node.value), None)

def evaluate_unary_expression(ast_node, environment):
    rt = evaluate(ast_node.value, environment)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    match rt.result.type.type:
        case "number":
            if ast_node.sign == "-":
                return RuntimeResult(create_number(-rt.result.value), None)
            
            return RuntimeResult(rt.result, None)
        case "boolean":
            if ast_node.sign == "-":
                return RuntimeResult(Boolean("false" if rt.result.value == "true" else "true"), None)
            
            return RuntimeResult(rt.result, None)
        case _:
            return RuntimeResult(None, DataTypeError(f"Unexpected unary operation for '{rt.result.type.type}'"))

def evaluate_binary_expression(ast_node, environment):
    rt = evaluate(ast_node.left, environment)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    left = rt.result
    
    rt = evaluate(ast_node.right, environment)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    right = rt.result

    match ast_node.operator:
        case "Plus":
            match left.type.type:
                case "number":
                    if right.type.type != "number":
                        return RuntimeResult(None, DataTypeError(f"Unexpected operation between number and {right.type.type}"))
                    
                    return RuntimeResult(create_number(left.value + right.value), None)
                case _:
                    return RuntimeResult(None, DataTypeError(f"Unexpected operation between number and {right.type.type}"))
        case "Minus":
            if left.type.type != "number" or right.type.type != "number":
                return RuntimeResult(None, DataTypeError(f"Unexpected operation between {left.type.type} and {right.type.type}"))
            
            return RuntimeResult(create_number(left.value - right.value), None)
        case "Multiply":
            if left.type.type != "number" or right.type.type != "number":
                return RuntimeResult(None, DataTypeError(f"Unexpected operation between {left.type.type} and {right.type.type}"))
            
            return RuntimeResult(create_number(left.value * right.value), None)
        case "Divide":
            if left.type.type != "number" or right.type.type != "number":
                return RuntimeResult(None, DataTypeError(f"Unexpected operation between {left.type.type} and {right.type.type}"))
            
            if right.value == 0:
                return RuntimeResult(None, MathError(f"Cannot divide {left.value} by 0"))
            
            return RuntimeResult(create_number(left.value / right.value), None)
        case "Power":
            if left.type.type != "number" or right.type.type != "number":
                return RuntimeResult(None, DataTypeError(f"Unexpected operation between {left.type.type} and {right.type.type}"))
            
            return RuntimeResult(create_number(left.value ** right.value), None)

def evaluate_variable_assignment(ast_node, environment):
    var_name = ast_node.var_name
    rt = evaluate(ast_node.value, environment)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    rt = environment.assign(var_name, rt.result)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    return RuntimeResult(rt.result, None)

def evaluate_variable_update(ast_node, environment):
    var_name = ast_node.var_name
    rt = evaluate(ast_node.value, environment)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    rt = environment.update(var_name, rt.result)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    return RuntimeResult(None, None)

def create_number(value):
    return Number(int(value) if value % 1 == 0 else value)