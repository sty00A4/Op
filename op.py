import sys, os, math
from typing import List

version = "1.0"

class Type:
    def __init__(self, type: str, line: int):
        if type == "int":
            self.type = Int
        elif type == "float":
            self.type = Float
        elif type == "bool":
            self.type = Bool
        elif type == "str":
            self.type = Str
        elif type == "getOp":
            self.type = GetOp
        elif type == "op":
            self.type = Op
        elif type == "funcOperation":
            self.type = FuncOp
        elif type == "obj":
            self.type = Obj
        elif type == "array":
            self.type = Array
        else:
            exception(f'unregistered type "{type}"', line)
    def __str__(self):
        return f"Type: {self.type}"
class Null:
    def __init__(self):
        self.val = None
class Int:
    def __init__(self, val: int):
        self.val = val
    def __str__(self):
        return f"Int: {self.val}"
class Float:
    def __init__(self, val: float):
        self.val = val
    def __str__(self):
        return f"Float: {self.val}"
class Bool:
    def __init__(self, val: bool):
        self.val = val
    def __str__(self):
        return f"Bool: {self.val}"
class Str:
    def __init__(self, val: str):
        self.val = val
    def __str__(self):
        return f"Str: '{self.val}'"
class Var:
    def __init__(self, name: str):
        self.name = name
    def __str__(self):
        return f"Var: {self.name} "
class Operator:
    def __init__(self, type: str):
        self.type = type
    def __str__(self):
        return f"Operator: {self.type}"
class Get:
    def __init__(self, type: str):
        self.type = type
    def __str__(self):
        return f"Get: {self.type}"
class GetOp:
    def __init__(self, op: list):
        self.val = op
    def __str__(self):
        text = "GetOp: "
        for line in self.val:
            text += " |" + str(line) + "| "
        return text[:-3]
class Op:
    def __init__(self, op: list[list]):
        self.val = op
    def __str__(self):
        text = "<"
        for j, line in enumerate(self.val):
            for i, token in enumerate(line):
                text += str(j) + "." + str(i) + " |" + str(token) + "| "
            text += "\n"
        text = text[:-1]
        text += ">"
        return text
class FuncArgs:
    def __init__(self, args: dict):
        self.args = args
class FuncOp:
    def __init__(self, op: list):
        self.val = op
    def __str__(self):
        text = "FuncOp: "
        for line in self.val:
            for token in line:
                text += " |" + str(token) + "| "
            text += " - "
        return text[:-3]
class Func:
    def __init__(self, args: FuncArgs, op: FuncOp):
        self.funcArgs = args
        self.funcOp = op
class Obj:
    def __init__(self, subs: dict):
        self.val = subs
class Array:
    def __init__(self, array: list):
        self.val = array
class Sep:
    def __init__(self):
        pass

class Grammar:
    def __init__(self):
        self.types = ["int", "float", "bool", "str", "nullType", "operator", "get", "op", "funcOperation", "getOp"]
        self.numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-"]
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                        't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                        'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '_']
        self.logics = ["true", "false"]
        self.builtinVars = ["sysArgs", "time"]
        self.operators = ["print", "set", "del", "inc" , "dec", "if", "else", "repeat", "while", "do", "return"]
        self.gets = ["add", "sub", "mul", "div", "pow", "sqrt", "round", "floor", "ceil", "abs",
                     "toint", "tofloat", "tobool", "tostr", "and", "or", "nand", "xor", "not", "equal",
                     "grtr", "less","grtrEqual", "lessEqual", "notEqual", "con", "func", "call"]
        self.all = ["int", "float", "bool", "str", "null", "operator", "get", "op", "get_op", "true", "false", "null", "print",
                    "set", "del", "if", "else", "elif", "add", "sub", "mul", "div", "pow", "sqrt", "round", "floor",
                    "ceil", "abs", "toint", "tofloat", "tobool", "tostr", "return", "and", "or", "nand", "xor", "not",
                    "equal", "grtr", "less","grtrEqual", "lessEqual", "null"]
        self.varTypes = [Int, Float, Bool, Str, GetOp, Op, FuncOp]
        self.getTypes = [GetOp, FuncOp, Int, Float, Bool, Str]
grammar = Grammar()

def exception(error: str, line: int):
    print(f"{error} (operation {line})")
    sys.exit()

def splits(text: str, seps: list):
    line = []
    temp = ""
    for i, c in enumerate(text):
        if c in seps:
            if not temp == "":
                line.append(temp)
                temp = ""
            line.append(c)
        else:
            temp += c
    if not temp == "":
        line.append(temp)
    return line
def removes(line: list, remove: list):
    rl = line
    for r in remove:
        while r in rl:
            rl.remove(r)
    return rl

def getToken(token, line: int, variables):
    if type(token) == Var:
        if token.name in variables:
            return variables[token.name], variables
        else:
            exception(f"'{token.name}' is not defined", line)
            return Null(), variables
    elif type(token) == GetOp:
        return getOperation(token.val, line, variables), variables
    elif type(token) == Func:
        return funcOperation(token.val, token.args, line, variables), variables
    elif type(token) in grammar.getTypes:
        return token, variables
    else:
        exception(f"expected Var, GetOp, FuncOp or any type, got {str(type(token))[17:-2]}", line)
        return Null(), variables

def funcOperation(op: List[list], args: dict, line: int, global_vars: dict = {}):
    line = 0
    not_delete = list(global_vars.keys())
    variables = global_vars
    for arg in args:
        variables[arg] = args[arg]
    delete = list(args.keys())
    returnToken = Null()
    while line < len(op):
        if type(op[line][0]) == Operator:
            operator = op[line][0]
            if operator.type == "set":
                if len(op[line]) > 2:
                    if type(op[line][1]) == Type:
                        if type(op[line][2]) == Var:
                            if type(op[line][3]) == GetOp:
                                variables[op[line][2].name] = getOperation(op[line][3].val, line, variables)
                            elif type(op[line][3]) == FuncOp:
                                variables[op[line][2].name] = funcOperation(op[line][3].val, line, variables)
                            else:
                                variables[op[line][2].name] = op[line][3]
                            delete.append(op[line][2].name)
                    elif type(op[line][1]) == Var:
                        if type(op[line][2]) == GetOp:
                            variables[op[line][1].name] = getOperation(op[line][2].val, line, variables)
                        elif type(op[line][2]) == FuncOp:
                            variables[op[line][1].name] = funcOperation(op[line][2].val, line, variables)
                        else:
                            variables[op[line][1].name] = op[line][2]
                        delete.append(op[line][1].name)
                    else:
                        exception(f"expected Var or Type for {operator.type}, got {str(type(op[line][1]))[17:-2]}",
                                  line)
                else:
                    exception(f"argument missing for {operator.type}", line)
            elif operator.type == "inc":
                # var
                if type(op[line][1]) == Var:
                    # int
                    if type(variables[op[line][1].name]) == Int:
                        # specific inc
                        if len(op[line]) > 2:
                            if type(op[line][2]) == Int:
                                if op[line][1].name in variables:
                                    variables[op[line][1].name].val += op[line][2].val
                                else:
                                    exception(f"'{op[line][1].name}' not defined", line)
                            else:
                                exception(f"expected Int for {operator.type}, got {str(type(op[line][2]))[17:-2]}",
                                          line)
                        else:
                            if op[line][1].name in variables:
                                variables[op[line][1].name].val += 1
                            else:
                                exception(f"'{op[line][1].name}' not defined", line)
                    else:
                        exception(
                            f"expected Int for {operator.type}, got {str(type(variables[op[line][1].name]))[17:-2]}",
                            line)
                else:
                    exception(f"expected Var for {operator.type}, got {str(type(op[line][1]))[17:-2]}", line)
            elif operator.type == "dec":
                # var
                if type(op[line][1]) == Var:
                    # int
                    if type(variables[op[line][1].name]) == Int:
                        # specific inc
                        if len(op[line]) > 2:
                            if type(op[line][2]) == Int:
                                if op[line][1].name in variables:
                                    variables[op[line][1].name].val -= op[line][2].val
                                else:
                                    exception(f"'{op[line][1].name}' not defined", line)
                            else:
                                exception(f"expected Int for {operator.type}, got {str(type(op[line][2]))[17:-2]}",
                                          line)
                        else:
                            if op[line][1].name in variables:
                                variables[op[line][1].name].val -= 1
                            else:
                                exception(f"'{op[line][1].name}' not defined", line)
                    else:
                        exception(
                            f"expected Int for {operator.type}, got {str(type(variables[op[line][1].name]))[17:-2]}",
                            line)
                else:
                    exception(f"expected Var for {operator.type}, got {str(type(op[line][1]))[17:-2]}", line)
            elif operator.type == "del":
                if len(op[line]) > 1:
                    if type(op[line][1]) == Var:
                        if op[line][1].name in variables:
                            variables.pop(op[line][1].name)
                        else:
                            exception(f"'{op[line][1].name}' not defined", line)
                    else:
                        exception(f"expected Var, got {str(type(op[line][1]))[17:-2]}", line)
            elif operator.type == "print":
                t1, variables = getToken(op[line][1], line, variables)
                if type(t1) == Bool:
                    if t1.val:
                        print("true")
                    else:
                        print("false")
                elif type(t1) == Null:
                    print("null")
                else:
                    print(t1.val)
            elif operator.type == "if":
                if len(op[line]) >= 2:
                    t1, variables = getToken(op[line][1], line, variables)
                else:
                    exception("missing argument for if", line)
                    return
                if len(op[line]) >= 3:
                    t2 = op[line][2]
                else:
                    exception("missing argument for if", line)
                    return
                if type(t1) == Bool:
                    if t1.val:
                        if type(op[line][2]) == Op:
                            returnToken, variables = funcOperation(t2.val, {}, line, variables)
                            if not type(returnToken) == Null:
                                break
                        else:
                            exception(f"expected Op, got {str(type(op[line + 1][1]))[17:-2]}", line)
                    else:
                        if len(op[line]) > 3:
                            if type(op[line][3]) == Operator:
                                if op[line][3].type == "else":
                                    if len(op[line]) > 4:
                                        if type(op[line][4]) == Op:
                                            t3 = op[line][4]
                                            returnToken, variables = funcOperation(t3.val, {}, line, variables)
                                            if not type(returnToken) == Null:
                                                break
                                        else:
                                            exception(f"expected Op, got {str(type(op[line][4]))[17:-2]}", line)
                                    else:
                                        exception("missing argument for else", line)
                                else:
                                    exception(f"expected else or new Operator, got {op[line][3].type}", line)
                            else:
                                exception(f"expected Operator, got {str(type(op[line][3]))[17:-2]}", line)
                else:
                    exception(f"expected Bool, got {str(type(t1))[17:-2]}", line)
            elif operator.type == "do":
                if len(op[line]) > 1:
                    t1 = op[line][1]
                    if type(t1) == Op:
                        variables = operation(t1.val, variables)
                    elif type(t1) == Var:
                        t1, variables = getToken(t1, line, variables)
                        if type(t1) == Op:
                            variables = operation(t1.val, variables)
                        else:
                            exception(f"expected Var with Op, got Var with {str(type(t1))[17:-2]}", line)
                    else:
                        exception(f"expected Op or Var with Op, got {str(type(t1))[17:-2]}", line)
                else:
                    exception(f"argument missing for do", line)
            elif operator.type == "repeat":
                if len(op[line]) >= 2:
                    t1, variables = getToken(op[line][1], line, variables)
                else:
                    exception("missing argument for repeat", line)
                    return
                if len(op[line]) >= 3:
                    t2 = op[line][2]
                else:
                    exception("missing argument for repeat", line)
                    return
                if type(t1) == Int:
                    if type(t2) == Op:
                        for i in range(t1.val):
                            returnToken, variables = funcOperation(t2.val, {}, line, variables)
                            if not type(returnToken) == Null:
                                break
                    else:
                        exception(f"expected Op, got {str(type(t2))[17:-2]}", line)
                else:
                    exception(f"expected Int, got {str(type(t2))[17:-2]}", line)
            elif operator.type == "while":
                if len(op[line]) > 1:
                    t1, variables = getToken(op[line][1], line, variables)
                else:
                    exception("missing argument for while", line)
                    return
                if len(op[line]) > 2:
                    t2 = op[line][2]
                else:
                    exception("missing argument for while", line)
                    return
                if type(t1) == Bool:
                    if type(t2) == Op:
                        while t1.val:
                            returnToken, variables = funcOperation(t2.val, {}, line, variables)
                            t1 = getToken(op[line][1], line, variables)
                            if not type(returnToken) == Null:
                                break
                        if not type(returnToken) == Null:
                            break
                    else:
                        exception(f"expected Op, got {str(type(t2))[17:-2]}", line)
                else:
                    exception(f"expected Bool or Var, got {str(type(t2))[17:-2]}", line)
            elif operator.type == "return":
                returnToken, variables = getToken(op[line][1], line, variables)
                break
            else:
                exception(f"unregistered Operator '{operator.type}'", line)
        else:
            exception(f"expected Operator, got {str(type(op[line][0]))[17:-2]}", line)
        line += 1
    for var in delete:
        if var in variables and not (var in not_delete):
            variables.pop(var)
    return returnToken, variables

def getOperation(op: list, line: int, global_vars: dict = {}):
    variables = global_vars
    if type(op[0]) == Get:
        get = op[0]
        if get.type == "add":
            if len(op) > 2:
                numbers = op[1:]
                temp = None
                type_ = "int"
                for number in numbers:
                    n, variables = getToken(number, line, variables)
                    if type(n) == Float:
                        type_ = "float"
                    if type(n) in [Int, Float]:
                        if temp:
                            temp += n.val
                        else:
                            temp = n.val
                    else:
                        exception(f"cannot add type {str(type(n))[17:-2]}", line)
                        return Null()
                if type_ == "float":
                    return Float(temp)
                else:
                    return Int(temp)
            else:
                exception(f"missing argument for {get.type}", line)
        elif get.type == "sub":
            if len(op) == 3:
                numbers = op[1:]
                temp = None
                type_ = "int"
                for number in numbers:
                    n, variables = getToken(number, line, variables)
                    if type(n) == Float:
                        type_ = "float"
                    if type(n) in [Int, Float]:
                        if temp:
                            temp -= n.val
                        else:
                            temp = n.val
                    else:
                        exception(f"cannot sub type {str(type(n))[17:-2]}", line)
                        return Null()
                if type_ == "float":
                    return Float(temp)
                else:
                    return Int(temp)
            else:
                exception(f"missing argument for {get.type}", line)
        elif get.type == "mul":
            if len(op) > 2:
                numbers = op[1:]
                temp = None
                type_ = "int"
                for number in numbers:
                    n, variables = getToken(number, line, variables)
                    if type(n) == Float:
                        type_ = "float"
                    if type(n) in [Int, Float]:
                        if temp:
                            temp *= n.val
                        else:
                            temp = n.val
                    else:
                        exception(f"cannot mul type {str(type(n))[17:-2]}", line)
                        return Null()
                if type_ == "float":
                    return Float(temp)
                else:
                    return Int(temp)
            else:
                exception(f"missing argument for {get.type}", line)
        elif get.type == "div":
            if len(op) > 2:
                numbers = op[1:]
                temp = None
                for number in numbers:
                    n, variables = getToken(number, line, variables)
                    if type(n) in [Int, Float]:
                        if temp:
                            temp /= n.val
                        else:
                            temp = n.val
                    else:
                        exception(f"cannot div type {str(type(n))[17:-2]}", line)
                        return Null()
                return Float(temp)
            else:
                exception(f"missing argument for {get.type}", line)
        elif get.type == "pow":
            if len(op) > 2:
                numbers = op[1:]
                temp = None
                type_ = "int"
                for number in numbers:
                    n, variables = getToken(number, line, variables)
                    if type(n) == Float:
                        type_ = "float"
                    if type(n) in [Int, Float]:
                        if temp:
                            temp = math.pow(temp, n.val)
                        else:
                            temp = n.val
                    else:
                        exception(f"cannot pow type {str(type(n))[17:-2]}", line)
                        return Null()
                if type_ == "float":
                    return Float(temp)
                else:
                    return Int(temp)
            else:
                exception(f"missing argument for {get.type}", line)
        elif get.type == "sqrt":
            if len(op) == 2:
                t1, variables = getToken(op[1], line, variables)
                if type(t1) in [Int, Float]:
                    return Float(math.sqrt(t1.val))
                else:
                    exception(f"cannot sqrt type {str(type(t1))[17:-2]}", line)
                    return Null()
            else:
                exception(f"missing argument for {get.type}", line)
        elif get.type == "floor":
            if len(op) == 2:
                t1, variables = getToken(op[1], line, variables)
                if type(t1) in [Int, Float]:
                    return Int(math.floor(t1.val))
                else:
                    exception(f"cannot floor type {str(type(t1))[17:-2]}", line)
                    return Null()
            else:
                exception(f"missing argument for {get.type}", line)
        elif get.type == "ceil":
            if len(op) == 2:
                t1, variables = getToken(op[1], line, variables)
                if type(t1) in [Int, Float]:
                    return Int(math.ceil(t1.val))
                else:
                    exception(f"cannot ceil type {str(type(t1))[17:-2]}", line)
                    return Null()
            else:
                exception(f"missing argument for {get.type}", line)
        elif get.type == "abs":
            if len(op) == 2:
                t1, variables = getToken(op[1], line, variables)
                if type(t1) == Int:
                    return Int(int(math.fabs(t1.val)))
                elif type(t1) == Float:
                    return Float(math.fabs(t1.val))
                else:
                    exception(f"cannot abs type {str(type(t1))[17:-2]}", line)
                    return Null()
            else:
                exception(f"missing argument for {get.type}", line)
        elif get.type == "mod":
            if len(op) > 2:
                numbers = op[1:]
                temp = 0
                type_ = "int"
                for number in numbers:
                    n, variables = getToken(number, line, variables)
                    if type(n) == Float:
                        type_ = "float"
                    if type(n) in [Int, Float]:
                        if temp:
                            temp %= n.val
                        else:
                            temp = n.val
                    else:
                        exception(f"cannot mul type {str(type(n))[17:-2]}", line)
                        return Null()
                if type_ == "float":
                    return Float(temp)
                else:
                    return Int(temp)
            else:
                exception(f"missing argument for {get.type}", line)
        elif get.type == "equal":
            if len(op) > 2:
                t1, variables = getToken(op[1], line, variables)
                t2, variables = getToken(op[2], line, variables)
                return Bool(t1.val == t2.val)
            else:
                exception(f"missing argument for {get.type}", line)
        elif get.type == "notEqual":
            if len(op) > 2:
                t1, variables = getToken(op[1], line, variables)
                t2, variables = getToken(op[2], line, variables)
                return Bool(t1.val != t2.val)
            else:
                exception(f"missing argument for {get.type}", line)
        elif get.type == "and":
            if len(op) > 2:
                t1, variables = getToken(op[1], line, variables)
                t2, variables = getToken(op[2], line, variables)
                return Bool(t1.val and t2.val)
            else:
                exception(f"missing argument for {get.type}", line)
        elif get.type == "or":
            if len(op) > 2:
                t1, variables = getToken(op[1], line, variables)
                t2, variables = getToken(op[2], line, variables)
                return Bool(t1.val or t2.val)
            else:
                exception(f"missing argument for {get.type}", line)
        elif get.type == "nand":
            if len(op) > 2:
                t1, variables = getToken(op[1], line, variables)
                t2, variables = getToken(op[2], line, variables)
                if t1.val == False and t2.val == False:
                    return Bool(True)
                if t1.val == True and t2.val == False:
                    return Bool(True)
                if t1.val == False and t2.val == True:
                    return Bool(True)
                if t1.val == True and t2.val == True:
                    return Bool(False)
            else:
                exception(f"missing argument for {get.type}", line)
        elif get.type == "xor":
            if len(op) > 2:
                t1, variables = getToken(op[1], line, variables)
                t2, variables = getToken(op[2], line, variables)
                if t1.val == False and t2.val == False:
                    return Bool(False)
                if t1.val == True and t2.val == False:
                    return Bool(True)
                if t1.val == False and t2.val == True:
                    return Bool(True)
                if t1.val == True and t2.val == True:
                    return Bool(False)
            else:
                exception(f"missing argument for {get.type}", line)
        elif get.type == "grtr":
            if len(op) > 2:
                t1, variables = getToken(op[1], line, variables)
                t2, variables = getToken(op[2], line, variables)
                return Bool(t1.val > t2.val)
            else:
                exception(f"missing argument for {get.type}", line)
        elif get.type == "less":
            if len(op) > 2:
                t1, variables = getToken(op[1], line, variables)
                t2, variables = getToken(op[2], line, variables)
                return Bool(t1.val < t2.val)
            else:
                exception(f"missing argument for {get.type}", line)
        elif get.type == "grtrEqual":
            if len(op) > 2:
                t1, variables = getToken(op[1], line, variables)
                t2, variables = getToken(op[2], line, variables)
                return Bool(t1.val >= t2.val)
            else:
                exception(f"missing argument for {get.type}", line)
        elif get.type == "lessEqual":
            if len(op) > 2:
                t1, variables = getToken(op[1], line, variables)
                t2, variables = getToken(op[2], line, variables)
                return Bool(t1.val <= t2.val)
            else:
                exception(f"missing argument for {get.type}", line)
        elif get.type == "not":
            if len(op) > 1:
                t1, variables = getToken(op[1], line, variables)
                if type(t1) == Bool:
                    return Bool(not t1.val)
                else:
                    exception(f"expected Bool, got {str(type(t1))[17:-2]}", line)
                    return Null()
            else:
                exception(f"missing argument for {get.type}", line)
        elif get.type == "toint":
            if len(op) > 1:
                t1, variables = getToken(op[1], line, variables)
                if type(t1) == Int:
                    return t1
                elif type(t1) == Float:
                    return Int(int(t1.val))
                elif type(t1) == Bool:
                    if t1.val:
                        return Int(1)
                    else:
                        return Int(0)
                elif type(t1) == Null:
                    return Int(0)
                else:
                    exception(f"expected Int, Float, Bool or Null, got {str(type(t1))[17:-2]}", line)
                    return Null()
            else:
                exception(f"missing argument for {get.type}", line)
        elif get.type == "tofloat":
            if len(op) > 1:
                t1, variables = getToken(op[1], line, variables)
                if type(t1) == Int:
                    return Float(float(t1.val))
                elif type(t1) == Float:
                    return t1
                else:
                    exception(f"expected Int or Float, got {str(type(t1))[17:-2]}", line)
                    return Null()
            else:
                exception(f"missing argument for {get.type}", line)
        elif get.type == "tobool":
            if len(op) > 1:
                t1, variables = getToken(op[1], line, variables)
                if type(t1) == Int:
                    return Bool(not t1.val == 0)
                elif type(t1) == Bool:
                    return t1
                elif type(t1) == Null:
                    return Bool(False)
                else:
                    exception(f"expected Int, Bool or NUll, got {str(type(t1))[17:-2]}", line)
                    return Null()
            else:
                exception(f"missing argument for {get.type}", line)
        elif get.type == "tostr":
            if len(op) > 1:
                t1, variables = getToken(op[1], line, variables)
                if type(t1) in [Int, Float, Str]:
                    return Str(str(t1.val))
                elif type(t1) == Bool:
                    if t1.val:
                        return Str("true")
                    else:
                        return Str("false")
                elif type(t1) == Null:
                    return Str("null")
                else:
                    exception(f"expected Int, Float, Str, Bool or Null, got {str(type(t1))[17:-2]}", line)
                    return Null()
            else:
                exception(f"missing argument for {get.type}", line)
        elif get.type == "con":
            if len(op) > 2:
                strings = op[1:]
                temp = ""
                for string in strings:
                    s, variables = getToken(string, line, variables)
                    if type(s) == Str:
                        temp += s.val
                    else:
                        exception(f"cannot add type {str(type(s))[17:-2]}", line)
                        return Null()
                return Str(temp)
            else:
                exception(f"missing argument for {get.type}", line)
        elif get.type == "func":
            if len(op) > 2:
                if type(op[1]) == FuncArgs:
                    if type(op[2]) == Op:
                        return Func(op[1], op[2])
                    else:
                        exception(f"expected FuncOp, got {str(type(op[2]))[17:-2]}", line)
                else:
                    exception(f"expected FuncArgs, got {str(type(op[1]))[17:-2]}", line)
            else:
                exception(f"missing argument for {get.type}", line)
        elif get.type == "call":
            if len(op) > 1:
                if type(op[1]) == Var:
                    t1, variables = getToken(op[1], line, variables)
                else:
                    t1 = op[1]
                if type(t1) == Func:
                    j = 0
                    inArgs = {}
                    for var in t1.funcArgs.args:
                        if len(op) >= 2+j:
                            inArgs[var] = op[2+j]
                        else:
                            exception("argument missing for function", line)
                        j += 1
                    returnToken, variables = funcOperation(t1.funcOp.val, inArgs, line, variables)
                    return returnToken
                else:
                    exception(f"expected Func, got {str(type(t1))[17:-2]}", line)
            else:
                exception(f"argument missing for {get.type}", line)
        else:
            exception(f"unregistered GetOp type {get.type}", line)
            return Null()
    else:
        exception(f"expected Get, got {str(type(op[0]))[17:-2]}", line)
        return Null()


def operation(op: List[list], global_vars: dict = {}, closed=True):
    line = 0
    not_delete = list(global_vars.keys())
    variables = global_vars
    delete = []
    while line < len(op):
        if type(op[line][0]) == Operator:
            operator = op[line][0]
            if operator.type == "set":
                if len(op[line]) > 2:
                    if type(op[line][1]) == Type:
                        if type(op[line][2]) == Var:
                            if type(op[line][3]) == GetOp:
                                variables[op[line][2].name] = getOperation(op[line][3].val, line, variables)
                            elif type(op[line][3]) == FuncOp:
                                variables[op[line][2].name] = funcOperation(op[line][3].val, line, variables)
                            else:
                                variables[op[line][2].name] = op[line][3]
                            delete.append(op[line][2].name)
                    elif type(op[line][1]) == Var:
                        if type(op[line][2]) == GetOp:
                            variables[op[line][1].name] = getOperation(op[line][2].val, line, variables)
                        elif type(op[line][2]) == FuncOp:
                            variables[op[line][1].name] = funcOperation(op[line][2].val, line, variables)
                        else:
                            variables[op[line][1].name] = op[line][2]
                        delete.append(op[line][1].name)
                    else:
                        exception(f"expected Var or Type for {operator.type}, got {str(type(op[line][1]))[17:-2]}", line)
                else:
                    exception(f"argument missing for {operator.type}", line)
            elif operator.type == "inc":
                # var
                if type(op[line][1]) == Var:
                    # int
                    if type(variables[op[line][1].name]) == Int:
                        # specific inc
                        if len(op[line]) > 2:
                            if type(op[line][2]) == Int:
                                if op[line][1].name in variables:
                                    variables[op[line][1].name].val += op[line][2].val
                                else:
                                    exception(f"'{op[line][1].name}' not defined", line)
                            else:
                                exception(f"expected Int for {operator.type}, got {str(type(op[line][2]))[17:-2]}", line)
                        else:
                            if op[line][1].name in variables:
                                variables[op[line][1].name].val += 1
                            else:
                                exception(f"'{op[line][1].name}' not defined", line)
                    else:
                        exception(f"expected Int for {operator.type}, got {str(type(variables[op[line][1].name]))[17:-2]}", line)
                else:
                    exception(f"expected Var for {operator.type}, got {str(type(op[line][1]))[17:-2]}", line)
            elif operator.type == "dec":
                # var
                if type(op[line][1]) == Var:
                    # int
                    if type(variables[op[line][1].name]) == Int:
                        # specific inc
                        if len(op[line]) > 2:
                            if type(op[line][2]) == Int:
                                if op[line][1].name in variables:
                                    variables[op[line][1].name].val -= op[line][2].val
                                else:
                                    exception(f"'{op[line][1].name}' not defined", line)
                            else:
                                exception(f"expected Int for {operator.type}, got {str(type(op[line][2]))[17:-2]}",
                                          line)
                        else:
                            if op[line][1].name in variables:
                                variables[op[line][1].name].val -= 1
                            else:
                                exception(f"'{op[line][1].name}' not defined", line)
                    else:
                        exception(
                            f"expected Int for {operator.type}, got {str(type(variables[op[line][1].name]))[17:-2]}",
                            line)
                else:
                    exception(f"expected Var for {operator.type}, got {str(type(op[line][1]))[17:-2]}", line)
            elif operator.type == "del":
                if len(op[line]) > 1:
                    if type(op[line][1]) == Var:
                        if op[line][1].name in variables:
                            variables.pop(op[line][1].name)
                        else:
                            exception(f"'{op[line][1].name}' not defined", line)
                    else:
                        exception(f"expected Var, got {str(type(op[line][1]))[17:-2]}", line)
            elif operator.type == "print":
                t1, variables = getToken(op[line][1], line, variables)
                if type(t1) == Bool:
                    if t1.val:
                        print("true")
                    else:
                        print("false")
                elif type(t1) == Null:
                    print("null")
                else:
                    print(t1.val)
            elif operator.type == "if":
                if len(op[line]) >= 2:
                    t1, variables = getToken(op[line][1], line, variables)
                else:
                    exception("missing argument for if", line)
                    return
                if len(op[line]) >= 3:
                    t2 = op[line][2]
                else:
                    exception("missing argument for if", line)
                    return
                if type(t1) == Bool:
                    if t1.val:
                        if type(op[line][2]) == Op:
                            variables = operation(t2.val, variables)
                        else:
                            exception(f"expected Op, got {str(type(op[line + 1][1]))[17:-2]}", line)
                    else:
                        if len(op[line]) > 3:
                            if type(op[line][3]) == Operator:
                                if op[line][3].type == "else":
                                    if len(op[line]) > 4:
                                        if type(op[line][4]) == Op:
                                            t3 = op[line][4]
                                            variables = operation(t3.val, variables)
                                        else:
                                            exception(f"expected Op, got {str(type(op[line][4]))[17:-2]}", line)
                                    else:
                                        exception("missing argument for else", line)
                                else:
                                    exception(f"expected else or new Operator, got {op[line][3].type}", line)
                            else:
                                exception(f"expected Operator, got {str(type(op[line][3]))[17:-2]}", line)
                else:
                    exception(f"expected Bool, got {str(type(t1))[17:-2]}", line)
            elif operator.type == "do":
                if len(op[line]) > 1:
                    t1 = op[line][1]
                    if type(t1) == Op:
                        variables = operation(t1.val, variables)
                    elif type(t1) == Func:
                        _, variables = funcOperation(t1.val, t1.args, line, variables)
                    elif type(t1) == Var:
                        t1, variables = getToken(t1, line, variables)
                        if type(t1) == Op:
                            variables = operation(t1.val, variables)
                        elif type(t1) == Func:
                            _, variables = funcOperation(t1.val, t1.args, line, variables)
                        else:
                            exception(f"expected Var with Op, got Var with {str(type(t1))[17:-2]}", line)
                    else:
                        exception(f"expected Op or Var with Op, got {str(type(t1))[17:-2]}", line)
                else:
                    exception(f"argument missing for do", line)
            elif operator.type == "repeat":
                if len(op[line]) >= 2:
                    t1, variables = getToken(op[line][1], line, variables)
                else:
                    exception("missing argument for repeat", line)
                    return
                if len(op[line]) >= 3:
                    t2 = op[line][2]
                else:
                    exception("missing argument for repeat", line)
                    return
                if type(t1) == Int:
                    if type(t2) == Op:
                        for i in range(t1.val):
                            variables = operation(t2.val, variables)
                    else:
                        exception(f"expected Op, got {str(type(t2))[17:-2]}", line)
                else:
                    exception(f"expected Int, got {str(type(t2))[17:-2]}", line)
            elif operator.type == "while":
                if len(op[line]) > 1:
                    t1, variables = getToken(op[line][1], line, variables)
                else:
                    exception("missing argument for while", line)
                    return
                if len(op[line]) > 2:
                    t2 = op[line][2]
                else:
                    exception("missing argument for while", line)
                    return
                if type(t1) == Bool:
                    if type(t2) == Op:
                        while t1.val:
                            variables = operation(t2.val, variables)
                            t1 = getToken(op[line][1], line, variables)
                    else:
                        exception(f"expected Op, got {str(type(t2))[17:-2]}", line)
                else:
                    exception(f"expected Bool or Var, got {str(type(t2))[17:-2]}", line)
            elif operator.type == "return":
                exception("Operator 'return' in Op", line)
            else:
                exception(f"unregistered Operator '{operator.type}'", line)
        else:
            exception(f"expected Operator, got {str(type(op[line][0]))[17:-2]}", line)
        line += 1
    if closed:
        for var in delete:
            if var in variables and not (var in not_delete):
                variables.pop(var)
    return variables

def tokenize(raw: list):
    op = [[]]
    i = 0
    line = 0
    while i < len(raw):
        if raw[i] == "\n":
            op.append([])
            line += 1
        elif raw[i] in grammar.operators:
            op[line].append(Operator(raw[i]))
        elif raw[i] in grammar.types:
            op[line].append(Type(raw[i], line))
        elif raw[i] in grammar.gets:
            op[line].append(Get(raw[i]))
        elif raw[i] in grammar.logics:
            op[line].append(Bool(raw[i] == "true"))
        elif raw[i][0] in grammar.letters:
            op[line].append(Var(raw[i]))
        elif raw[i][0] in grammar.numbers:
            if "." in raw[i]:
                op[line].append(Float(float(raw[i])))
            else:
                op[line].append(Int(int(raw[i])))
        elif raw[i] == '"':
            text = ""
            i += 1
            while i < len(raw) and not raw[i] == '"':
                text += raw[i]
                i += 1
            op[line].append(Str(text))
        elif raw[i] == "<":
            count = 1
            temp = []
            i += 1
            while i < len(raw) and count > 0:
                temp.append(raw[i])
                if raw[i] == "<": count += 1
                if raw[i] == ">": count -= 1
                i += 1
            op_ = tokenize(temp[:-1]).val
            # operation type
            if type(op_[0][0]) == Operator:
                op[line].append(Op(op_))
            elif type(op_[0][0]) == Get and len(op_) == 1:
                op[line].append(GetOp(op_[0]))
            else:
                exception("no valid operation", line)
            i -= 1
        elif raw[i] == "(":
            count = 1
            temp = []
            i += 1
            while i < len(raw) and count > 0:
                temp.append(raw[i])
                if raw[i] == "(": count += 1
                if raw[i] == ")": count -= 1
                i += 1
            args = tokenize(temp[:-1]).val
            # operation type
            if type(args[0][0]) == Var:
                funcArgs = {}
                for v in args[0]:
                    if type(v) == Var:
                        funcArgs[v.name] = Null()
                    else:
                        exception(f"expected Var, got {str(type(v))[17:-2]}", line)
                op[line].append(FuncArgs(funcArgs))
            else:
                exception(f"expected Type or Var, got {str(type(args[0][0]))[17:-2]}", line)
            i -= 1
        elif raw[i] == ",":
            op[line].append(Sep())
        elif raw[i] in [" ", "\t", "\r"]:
            pass
        else:
            exception(f"{raw[i]} not recognized", line)
        i += 1
    removes(op, [[]])
    return Op(op)

if len(sys.argv) > 1:
    dev = False
    if len(sys.argv) > 2:
        dev = sys.argv[2] == "-dev"
    with open(sys.argv[1], "r") as f:
        # get the raw script in list form
        spliters = [" ", "\t", "\r" ,"\n", "<", ">", ",", '"', "(", ")"]
        spliters.extend(grammar.all)
        raw = splits(f.read(), spliters)
        # generate tokens and catch errors
        main_op = tokenize(raw)
        # print raw
        if dev:
            print(f"OP Version: {version}")
            print("---- Raw ----")
            print(removes(raw, [" ", "\t"]))
            # print tokens
            print("---- Tokens ----")
            print(main_op)
            # execute main operation
            print("---- Operation ----")
        print("")
        variables = operation(main_op.val, {}, False)
        if dev:
            print("")
            print("---- Variables ----")
            print(variables)
            print("")