# Constants
from typing import Dict


TOKEN_LEFT_PARANT = 0
TOKEN_RIGHT_PARANT = 1
TOKEN_CONSTANT_NUMBER = 3
TOKEN_CONSTANT_STRING = 4
TOKEN_IDENTIFIER = 5
TOKEN_EOF = 6
TOKEN_PLUS = 7
TOKEN_MINUS = 8
TOKEN_PRODUCT = 9
TOKEN_DIVIDE = 10
TOKEN_IDENTIFIER = 11
TOKEN_POW = 12

# Class Token


class Token:
    def __init__(self, type: int, content: str):
        self.type = type
        self.content = content

    def __str__(self):
        return f"Content: {self.content} - Type: {self.type}"
# -------------------------------------------


# Class Lexer
class Lexer:
    state: int = -1
    source: str = ""

    def __init__(self, source: str):
        self.state = -1
        self.source = source

    def reset(self):
        self.state = 0

    def eat(self):
        if self.state + 1 < len(self.source):
            self.state = self.state + 1
            return self.source[self.state]
        else:
            return None

    def putback(self):
        self.state = self.state - 1
        if self.state < -1:
            self.state = -1

    def lookforward(self):
        if self.state + 1 < len(self.source):
            return self.source(self.state + 1)
        else:
            return None

    def nextToken(self):
        cc = self.eat()
        if cc == None:
            return Token(TOKEN_EOF, "-EOF-")
        elif cc.isspace():
            return self.nextToken()
        elif cc == '(':
            return Token(TOKEN_LEFT_PARANT, "(")
        elif cc == ')':
            return Token(TOKEN_RIGHT_PARANT, ")")
        elif cc == '+':
            return Token(TOKEN_PLUS, "+")
        elif cc == '-':
            return Token(TOKEN_MINUS, "-")
        elif cc == '*':
            return Token(TOKEN_PRODUCT, "*")
        elif cc == '/':
            return Token(TOKEN_DIVIDE, "/")
        elif cc == '^':
            return Token(TOKEN_POW, "^")
        elif cc.isnumeric():
            content = cc
            while True:
                cc = self.eat()
                if cc.isnumeric() or cc == ".":
                    content = content + cc
                else:
                    self.putback()
                    break
            if content.count(".") > 0:
                return Token(TOKEN_CONSTANT_NUMBER, float(content))
            else:
                return Token(TOKEN_CONSTANT_NUMBER, int(content))
        elif cc.isalnum:
            content = cc
            while True:
                cc = self.eat()
                if cc.isalnum():
                    content = content + cc
                else:
                    self.putback()
                    break
            return Token(TOKEN_IDENTIFIER, content)

        else:
            return Token(TOKEN_EOF, None)
# -------------------------------------------------------------------

# class Expression


class Expression():
    def eval(self, environment: Dict):
        pass


class NumberExpression(Expression):
    def __init__(self, val):
        self.val = val

    def eval(self, environment: Dict):
        return self.val


class BinaryOperatorExpression(Expression):
    def __init__(self, op: str, left: Expression, right: Expression):
        self.op = op
        self.left = left
        self.right = right

    def eval(self, env: Dict):
        if self.op == "+":
            return self.left.eval(env) + self.right.eval(env)
        elif self.op == "-":
            return self.left.eval(env) - self.right.eval(env)
        elif self.op == "*":
            return self.left.eval(env) * self.right.eval(env)
        elif self.op == "/":
            return self.left.eval(env) / self.right.eval(env)
        elif self.op == "^":
            return self.left.eval(env) ** self.right.eval(env)
        else:
            return ErrorExpression(f"Operator not defined yet: {self.op}")


class ErrorExpression(Expression):
    def __init__(self, msg):
        self.msg = msg

    def eval(self, env: Dict):
        return self.msg


class IdentifierExpression(Expression):
    def __init__(self, id: str):
        self.id = id

    def eval(self, env: Dict):
        return env[self.id]


class DefExpression(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env: Dict):
        val = self.right.eval(env)
        env[self.left.id] = val
        return val


class ListExpression(Expression):
    def __init__(self, listcontent: [Expression]):
        self.listcontent = listcontent

    def eval(self, env: Dict):
        return [elem.eval(env) for elem in self.listcontent]


class LengthExpression(Expression):
    def __init__(self, listExpr):
        self.listExpr = listExpr

    def eval(self, env: Dict):
        return len(self.listExpr.eval(env))


class DumpExpression(Expression):
    def eval(self, env: Dict):
        return str(env)


class FunctionExpression(Expression):
    def __init__(self, paramlist: ListExpression, body: Expression):
        self.paramlist = paramlist
        self.body = body

    def eval(self, env: Dict):
        return self


class FunctionCallExpression(Expression):
    def __init__(self, fname: IdentifierExpression, args: ListExpression):
        self.fname = fname
        self.args = args

    def eval(self, env: Dict):
        fdict = dict()
        func: FunctionExpression = env[self.fname.id]
        for i in range(0, len(func.paramlist.listcontent)):
            fdict[func.paramlist.listcontent[i].id] = self.args.listcontent[i].eval(
                fdict)
        result = func.body.eval(fdict)
        return result

# --------------------------------------------------------------------


class Parser():
    def __init__(self, code):
        self.lexer = Lexer(code)
        self.tokens = []
        self.state = -1
        while True:
            tok = self.lexer.nextToken()
            self.tokens.append(tok)
            if tok.type == TOKEN_EOF:
                break

    def getNextToken(self):
        self.state = self.state + 1
        if self.state > len(self.tokens) - 1:
            return Token(TOKEN_EOF, None)
        return self.tokens[self.state]

    def eatRightParanth(self):
        token = self.getNextToken()
        if not (token.type == TOKEN_RIGHT_PARANT):
            raise Exception(f"Right paranthesis expected but {token} found")

    def parseNextExpression(self):
        token = self.getNextToken()
        if token.type == TOKEN_LEFT_PARANT:
            return self.parseNextExpression()
        elif token.type == TOKEN_RIGHT_PARANT:
            return None
        elif token.type == TOKEN_CONSTANT_NUMBER:
            return NumberExpression(token.content)
        elif token.type == TOKEN_PLUS:
            left = self.parseNextExpression()
            right = self.parseNextExpression()
            self.eatRightParanth()
            return BinaryOperatorExpression("+", left, right)
        elif token.type == TOKEN_PRODUCT:
            left = self.parseNextExpression()
            right = self.parseNextExpression()
            self.eatRightParanth()
            return BinaryOperatorExpression("*", left, right)
        elif token.type == TOKEN_MINUS:
            left = self.parseNextExpression()
            right = self.parseNextExpression()
            self.eatRightParanth()
            return BinaryOperatorExpression("-", left, right)
        elif token.type == TOKEN_DIVIDE:
            left = self.parseNextExpression()
            right = self.parseNextExpression()
            self.eatRightParanth()
            return BinaryOperatorExpression("/", left, right)
        elif token.type == TOKEN_POW:
            left = self.parseNextExpression()
            right = self.parseNextExpression()
            self.eatRightParanth()
            return BinaryOperatorExpression("^", left, right)
        elif token.type == TOKEN_IDENTIFIER:
            if token.content == "def":
                left = self.parseNextExpression()
                right = self.parseNextExpression()
                self.eatRightParanth()
                return DefExpression(left, right)
            elif token.content == "list":
                listcontent = []
                while True:
                    exxpr = self.parseNextExpression()
                    if exxpr == None:
                        break
                    listcontent.append(exxpr)
                return ListExpression(listcontent)
            elif token.content == "length":
                arg = self.parseNextExpression()
                self.eatRightParanth()
                return LengthExpression(arg)
            elif token.content == "dump":
                self.eatRightParanth()
                return DumpExpression()
            elif token.content == "fn":
                paramlist = self.parseNextExpression()
                body = self.parseNextExpression()
                self.eatRightParanth()
                return FunctionExpression(paramlist, body)
            elif token.content == "funcall":
                fname = self.parseNextExpression()
                arglist = self.parseNextExpression()
                self.eatRightParanth()
                return FunctionCallExpression(fname, arglist)
            else:
                return IdentifierExpression(token.content)
        elif token.type == TOKEN_EOF:
            return None
        else:
            print(f"Parser: What '{token}'?")
            return None

    def __str__(self):
        return str([str(t) for t in self.tokens])

# ---------------------------------------------------------------------


class Interpreter:
    def __init__(self):
        self.env = dict()

    def interprete(self, code: str):
        parser = Parser(code)
        result: Expression = None
        while True:
            expr = parser.parseNextExpression()
            if expr == None:
                break
            result = expr.eval(self.env)
        return result


#code = "(length (list 1 2 3 4 5 ))"
#parser = Parser(code)
# print(parser.parseNextExpression())


# REPL
#interpreter = Interpreter()
# code = """
# (def f (fn (list x) (* x 2)))
# (funcall f (list 5))
# """
# print(interpreter.interprete(code))
# while True:
#    inp = input("lambada> ")
#    print(interpreter.interprete(inp))
