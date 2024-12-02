from .frontend.lexer import tokenize
from .frontend.parser import Parser
from .runtime.interpreter import evaluate
from .runtime.values import Environment

def execute_code(text):
    global_environment = Environment()
    rt = tokenize(text)
    if rt.error:
        rt.error.show_error()
    
    parser = Parser(rt.result)
    rt = parser.produce_ast()
    if rt.error:
        rt.error.show_error()
    print(rt.result)
    rt = evaluate(rt.result, global_environment)
    if rt.error:
        rt.error.show_error()
    
    print(rt.result)