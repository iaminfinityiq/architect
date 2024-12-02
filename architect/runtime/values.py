from ..errors import RuntimeResult, VariableError

class Environment:
    def __init__(self, parent=None):
        self.table = {}
        self.parent = parent
    
    def lookup(self, var_name):
        if var_name not in self.table:
            if not self.parent:
                return RuntimeResult(None, VariableError(f"Cannot get the value of variable {var_name} because it does not exist."))

            rt = self.parent.resolve(var_name)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(rt.result, None)
        
        return RuntimeResult(self.table[var_name], None)

    def update(self, var_name, value):
        if var_name not in self.table:
            return RuntimeResult(None, VariableError(f"Cannot update variable {var_name} because it does not exist."))
        
        self.table[var_name] = value
        return RuntimeResult(None, None)
    
    def assign(self, var_name, value):
        if var_name in self.table:
            return RuntimeResult(None, VariableError(f"Cannot assign variable {var_name} because it existS."))
        
        self.table.update({var_name: value})
        return RuntimeResult(None, None)

class ValueType:
    def __init__(self, type):
        self.type = type

class RuntimeValue:
    def __init__(self, type):
        self.type = type

class Number(RuntimeValue):
    def __init__(self, value):
        super().__init__(ValueType("number"))
        self.value = value
    
    def __repr__(self):
        return str(self.value)

class Boolean(RuntimeValue):
    def __init__(self, value):
        super().__init__(ValueType("boolean"))
        self.value = value
    
    def __repr__(self):
        return self.value

class Null(RuntimeValue):
    def __init__(self):
        super().__init__(ValueType("null"))
    
    def __repr__(self):
        return "null"