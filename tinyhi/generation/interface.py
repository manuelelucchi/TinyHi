import tinyhi.generation.nodes as n
from .error import *
from typing import List

"""
In questo modulo si trovano le interfacce per la semplificazione della creazione di nodi per la generazione partendo dall'albero di parsing
"""

# AST Utils


def Build(node: n.ExpressionNode, children: List[n.ASTNode]) -> n.ASTNode:
    node.children = children
    return node

# Program Utils


def Program(*args):
    args: List[n.FunctionDefinitionNode] = list(args)
    # Set Collect of global variables
    args[-1].children = args[-1].children[:-1] + \
        [CollectGlobals()] + [args[-1].children[-1]]
    return Build(n.ProgramNode(), list(args))


# Function Utils

def Function(name, args):
    def Body(*body):
        body = [n.ActivateNode()] + list(body)
        return Build(n.FunctionDefinitionNode(name, list(args)), body)
    return Body


def Call(name):
    def _Call(*args):
        return Build(n.FunctionCallNode(name), Objects(list(args)))
    return _Call


def Nothing():
    return Block()


def Block(*args):
    return Build(n.BlockNode(), list(args))


def Return(variable=None):
    if variable is None:
        raise ReturnError()
    else:
        return Build(n.ReturnNode(), [Object(variable)])


def CollectGlobals():
    return n.CollectGlobalsNode()

# Reference


def Variable(name):
    if not isinstance(name, str):
        raise ValueError("Name should be a string")
    return n.ReferenceNode(name)

# Literals


def StringLiteral(value=""):
    return n.StringConstantNode(value)


def IntLiteral(value=0):
    return n.IntConstantNode(value)

# Assignment


def Assign(variable, value=None):
    if not isinstance(variable, str):
        raise ValueError("Variable should be a string")
    right = None
    if issubclass(type(value), n.ASTNode):
        right = [Object(value)]
    elif value is None:
        right = []
    else:
        raise AssignValueError(value, variable)
    return Build(n.AssignmentNode(variable), right)

# Unnamed


def Int(value: int = 0):
    if not isinstance(value, (int, n.IntConstantNode)):
        raise ValueError("Name should be an int or an IntConstantNode")
    i = IntLiteral(value) if isinstance(value, int) else value
    return Build(n.AllocIntNode(), [i])


def String(value: str = ""):
    if not isinstance(value, (str, n.StringConstantNode)):
        raise ValueError("Name should be a string or a StringConstantNode")
    s = StringLiteral(value) if isinstance(value, str) else value
    return Build(n.AllocStringNode(), [s])


def TryOptimize(values: list):
    if all(map(lambda x: isinstance(x, (str, n.StringConstantNode)), values)):
        accum = ""
        for x in values:
            accum += x.value if isinstance(x, n.StringConstantNode) else x
        return String(accum)

    if any(map(lambda x: isinstance(x, (int, n.IntConstantNode)), values)) and any(map(lambda x: isinstance(x, (str, n.StringConstantNode)), values)):
        raise ConcatenationError()

    return None


def Vector(value):
    if not isinstance(value, list):
        raise ValueError("Name should be a list")

    possible = TryOptimize(value)
    if possible is not None:
        return possible
    values = Variadic(value)

    return Build(n.AllocVectorNode(), [IntLiteral(len(value))] + values)


def Object(value):
    if isinstance(value, list):
        return Vector(value)
    elif isinstance(value, (str, n.StringConstantNode)):
        return String(value)
    elif isinstance(value, (int, n.IntConstantNode)):
        return Int(value)
    elif issubclass(type(value), n.ASTNode):
        return value
    else:
        raise ValueError(
            "Value should be either an int, a list, a string or an ASTNode")


def Objects(values):
    return list(map(Object, values))


def Variadic(values):
    if not isinstance(values, list):
        raise ValueError("Value should be a list")
    l = list()
    for v in values:
        ty = None
        val = None
        if isinstance(v, str):
            ty = IntLiteral(2)
            val = StringLiteral(v)
        elif isinstance(v, int):
            ty = IntLiteral(0)
            val = IntLiteral(v)
        elif isinstance(v, n.StringConstantNode):
            ty = IntLiteral(2)
            val = v
        elif isinstance(v, n.IntConstantNode):
            ty = IntLiteral(0)
            val = v
        elif issubclass(type(v), (n.ASTNode)):
            ty = IntLiteral(1)
            val = v
        else:
            raise ValueError(
                "Value should contains either an int, a string or an ASTNode")
        l += [ty, val]
    return l


# I/O


def Input():
    return n.InputNode()


def Output(variable):
    return Build(n.OutputNode(), [
        Object(variable)
    ])

# Compare


def _UnaryOperation(nodeType, right):
    return Build(nodeType(), [
        Object(right)
    ])


def Length(value):
    return _UnaryOperation(n.LengthNode, value)


def Negation(value):
    return _UnaryOperation(n.NegationNode, value)

# Compare


def _CompareOperation(nodeType, left, right):
    return Build(nodeType(), [
        Object(left),
        Object(right)
    ])


def Equals(left, right):
    return _CompareOperation(n.EqualsNode, left, right)


def NotEquals(left, right):
    return _CompareOperation(n.NotEqualsNode, left, right)


def MoreThan(left, right):
    return _CompareOperation(n.MoreThanNode, left, right)


def MoreEqual(left, right):
    return _CompareOperation(n.MoreEqualNode, left, right)


def LessThan(left, right):
    return _CompareOperation(n.LessThanNode, left, right)


def LessEqual(left, right):
    return _CompareOperation(n.LessEqualNode, left, right)

# Math


def _MathOperation(nodeType, left, right):
    return Build(nodeType(), [
        Object(left),
        Object(right)
    ])


def Sum(left, right):
    return _MathOperation(n.SumNode, left, right)


def Sub(left, right):
    return _MathOperation(n.SubNode, left, right)


def Mul(left, right):
    return _MathOperation(n.MulNode, left, right)


def Div(left, right):
    return _MathOperation(n.DivNode, left, right)

# Enumeration Operations


def Subscripting(inp, indexes):
    input_var = Object(inp)

    def ToIndex(x):
        if isinstance(x, int):
            return [IntLiteral(0), IntLiteral(x)]
        elif isinstance(x, n.IntConstantNode):
            return [IntLiteral(0), x]
        elif isinstance(x, n.ReferenceNode):
            return [IntLiteral(1), x]
        else:
            val = x
            if issubclass(type(x), n.StringConstantNode):
                val = "\"" + x.value + "\""
            elif issubclass(type(x), n.IntConstantNode):
                val = x.value
            raise SubscriptingError(val, input_var.name)

    indexes_vars = []
    for x in indexes:
        indexes_vars += ToIndex(x)

    return Build(n.SubscriptingNode(), [
        input_var,
        IntLiteral(len(indexes))
    ] + indexes_vars)


# Control Flow


def If(cond, iftrue, iffalse=None):
    cond = Block(n.ActivateNode(), cond)
    args = [cond, iftrue] if iffalse is None else [cond, iftrue, iffalse]
    return Build(n.IfNode(), args)


def While(cond, body):
    body = Block(n.ActivateNode(), body)
    args = [cond, body]
    return Build(n.WhileNode(), args)


def Until(cond, body):
    body = Block(n.ActivateNode(), body)
    args = [cond, body]
    return Build(n.UntilNode(), args)
