from tinyhi.generation import *
from .context import *
from tinyhi.parsing import *
from .error import *


def AST(tree):
    """
    Genera l'AST a partire dal parsing tree
    """
    ast = None
    try:
        init()
        ctx = ParsingContext()
        ast = visit(tree, ctx)
    except Exception as e:
        print("AST Generation Failed")
        print("{}: {}".format(type(e).__name__, e))
    finally:
        return ast


rules = dict()
tokens = dict()


def init():
    """
    Costruisce due dispatch table, una per le regole e una per i tokens.
    """
    global rules
    if len(rules) == 0:
        rules[program_rule] = _Program
        rules[function_rule] = _Function
        rules[function_args_rule] = _FunctionArgs
        rules[functions_rule] = _Functions
        rules[block_rule] = _Block
        rules[expressions_rule] = _Expressions
        rules[expr_rule] = _Expr
        rules[control_rule] = _Control
        rules[statement_rule] = _Statement
        rules[assignment_rule] = _Assignment
        rules[condition_rule] = _ConditionOperation
        rules[while_rule] = _While
        rules[until_rule] = _Until
        rules[if_rule] = _If
        rules[else_rule] = _Else
        rules[brackets_rule] = _Brackets
        rules[function_call_rule] = _FunctionCall
        rules[input_rule] = _Input
        rules[subscripting_rule] = _Subscripting
        rules[call_args_rule] = _CallArgs

    global tokens
    if len(tokens) == 0:
        tokens[name_token] = _Name
        tokens[string_token] = _String
        tokens[int_token] = _Int
        tokens[condition_op_token] = _ConditionOperator


def visit(tree, ctx: ParsingContext):
    global rules
    global tokens

    f = None
    if tree.root['type'] == 'rule':
        f = rules.get(tree.root['rule'])
        if f is None:
            raise UndefinedRuleError(tree.root['rule'])
    elif tree.root['type'] == 'token':
        f = tokens.get(tree.root['name'])
        if f is None:
            raise UndefinedTokenError(tree.root['value'])

    if f is None:
        raise NotRuleOrTokenError(tree.root['type'])
    return f(tree, ctx)


def is_token(node, name):
    if node.root['type'] == 'token':
        return node.root['name'] == name
    else:
        return False


def is_rule(node, rule):
    if node.root['type'] == 'rule':
        return node.root['rule'] == rule
    else:
        return False


def is_global(name):
    return name[0] == '.'


def remove_returns(children):
    return list(filter(lambda x: not is_token(x, return_token), children))


def can_call_function(name, ctx: ParsingContext):
    counter = 0
    fun = 0
    # Se chiama se stessa o una funzione globale restituisci true
    if ctx.current_function_name == name or is_global(name):
        return True
    while True:
        t = tuple(ctx.current_scopes[0:-1] + [counter])
        fun = ctx.functions.get(t)
        if fun is None:
            break
        if fun.name == name:
            return True
        counter += 1
    counter = 0
    while True:
        t = tuple(ctx.current_scopes + [counter])
        fun = ctx.functions.get(t)
        if fun is None:
            return False
        if fun.name == name:
            return True
        counter += 1


def _Program(tree, ctx: ParsingContext):
    children = remove_returns(tree.children)
    ctx.start_function(0)
    visit(children[0], ctx)
    ctx.end_function()
    return Program(*ctx.get_functions())


def _Function(tree, ctx: ParsingContext):
    children = remove_returns(tree.children)
    name = children[1].root['value']

    prev = ctx.current_function_name

    # Assegna la funzione come corrente
    ctx.current_function_name = name

    third_children = children[2]

    args = visit(third_children, ctx) if is_rule(
        third_children, function_args_rule) else []

    fourth_children = children[3]

    body_tree = third_children if is_rule(
        third_children, block_rule) else None

    body_tree = fourth_children if is_rule(
        fourth_children, block_rule) else body_tree

    body = visit(body_tree, ctx) if body_tree is not None else []

    # Inserisce prima del corpo la creazione della variabile di return e dopo il corpo il restituire la variabile di return
    body = [Assign(name, Int(0))] + body + [Return(Variable(name))]

    fun = Function(name, args)(*body)

    ctx.add_function(fun)

    # Riassegna la funzione precedente come corrente
    ctx.current_function_name = prev

    return Nothing()


def _Block(tree, ctx: ParsingContext):
    visit(tree.children[0], ctx)
    return visit(tree.children[1], ctx)


def _Expr(tree, ctx: ParsingContext):
    value = visit(tree.children[0], ctx)
    if is_rule(tree.children[0], statement_rule):
        return Output(value)
    else:
        return value


def _Control(tree, ctx: ParsingContext):
    return visit(tree.children[0], ctx)


def _FunctionArgs(tree, ctx: ParsingContext):
    return list(map(lambda x: x.root['value'], filter(lambda child: is_token(child, name_token), tree.children)))


def _Functions(tree, ctx: ParsingContext):
    func_counter = 0
    for child in tree.children:
        ctx.start_function(func_counter)
        visit(child, ctx)
        func_counter += 1
        ctx.end_function()


def _Expressions(tree, ctx: ParsingContext):
    exprs = list(map(lambda c: visit(c, ctx), tree.children))
    return exprs


def _Brackets(tree, ctx: ParsingContext):
    return visit(tree.children[1], ctx)


def _Assignment(tree, ctx: ParsingContext):
    name = visit(tree.children[0], ctx)
    value = tree.children[2] if len(tree.children) == 3 else None
    value_ast = visit(value, ctx) if value is not None else None
    if isinstance(value_ast, list):
        value_ast = Vector(value_ast)
    return Assign(name, value_ast)


def _Input(tree, ctx: ParsingContext):
    name = visit(tree.children[1], ctx)
    return Assign(name, Input())


def _FunctionCall(tree, ctx: ParsingContext):
    name = visit(tree.children[0], ctx)
    if not can_call_function(name, ctx):
        raise IllegalFunctionCallError(ctx.current_function_name, name)
    args = visit(tree.children[2], ctx) if is_rule(
        tree.children[2], call_args_rule) else []
    return Call(name)(*args)


def _CallArgs(tree, ctx: ParsingContext):
    return list(map(lambda x: visit(x, ctx), filter(lambda y: is_rule(y, statement_rule), tree.children)))


def _Name(tree, ctx: ParsingContext):
    return tree.root['value']


def _Statement(tree, ctx: ParsingContext):
    # Se e' lungo 1 allora e' gestito automaticamente da visit
    if len(tree.children) == 1:
        value = visit(tree.children[0], ctx)
        if isinstance(value, str):
            return Variable(value)
        else:
            return value
    # Se sono lunghi piu' di uno e sono tutti statement allora e' per forza una concatenazione
    elif all(map(lambda x: is_rule(x, statement_rule), tree.children)):
        res = []
        for child in tree.children:
            v = visit(child, ctx)
            if isinstance(v, list):
                res += v
            else:
                res.append(v)
        return res
    # se non e' una concatenazione e sono due nodi, e' un'operazione unaria (token statement)
    elif len(tree.children) == 2:
        return _UnaryOperation(tree, ctx)
    # Se non e' una concatenazione e sono tre nodi, e' un'operazione binaria (statement token statement)
    elif len(tree.children) == 3:
        return _MathOperation(tree, ctx)
    else:
        raise ASTGenerationError(tree)

# Unary


def _UnaryOperator(tree, ctx: ParsingContext):
    op = tree.root['value']
    if op == '#':
        return Length
    elif op == '~':
        return Negation
    else:
        raise UndefinedTokenError(op)


def TryOptimizeLength(value):
    if isinstance(value, list):
        # Se e' una lista di interi, li conta
        if all(map(lambda x: isinstance(x, (n.IntConstantNode, int)), value)):
            return IntLiteral(len(value))
        # Se e' una lista di stringhe, somma la lunghezza di ogni stringhe
        elif all(map(lambda x: isinstance(x, (n.StringConstantNode, str)), value)):
            accum = 0
            for s in value:
                accum += len(s)
            return IntLiteral(accum)
        else:
            return None
    # Se e' un intero restituisce 1
    elif isinstance(value, (n.IntConstantNode, int)):
        return IntLiteral(1)
    # Se e' una stringa, restituisce la lunghezza
    elif isinstance(value, (n.StringConstantNode, str)):
        if isinstance(value, n.StringConstantNode):
            return IntLiteral(len(value.value))
        else:
            return IntLiteral(len(value))
    else:
        return None


def TryOptimizeNegation(value):
    if isinstance(value, list):
        if all(map(lambda x: isinstance(x, (n.IntConstantNode, int)), value)):
            return list(map(lambda x: IntLiteral(-x.value) if isinstance(x, n.IntConstantNode) else IntLiteral(-x), value))
        elif all(map(lambda x: isinstance(x, (n.StringConstantNode, str)), value)):
            raise NegateError()
    elif isinstance(value, (n.IntConstantNode, int)):
        if isinstance(value, n.IntConstantNode):
            return IntLiteral(value.value)
        else:
            return IntLiteral(value)
    elif isinstance(value, (n.StringConstantNode, str)):
        raise NegateError()
    else:
        return None


def TryOptimizeUnary(tree, value):
    op = tree.root['value']
    if op == '#':
        return TryOptimizeLength(value)
    elif op == '~':
        return TryOptimizeNegation(value)
    else:
        raise UndefinedTokenError(op)


def _UnaryOperation(tree, ctx: ParsingContext):
    [op, right] = tree.children
    right_node = visit(right, ctx)
    possible = TryOptimizeUnary(op, right_node)
    if possible is not None:
        return possible
    fun = _UnaryOperator(op, ctx)
    return fun(right_node)

# Math


def _MathOptimization(tree, ctx: ParsingContext):
    op = tree.root['value']
    if op == '+':
        return lambda a, b: IntLiteral(a+b)
    elif op == '-':
        return lambda a, b: IntLiteral(a-b)
    elif op == '*':
        return lambda a, b: IntLiteral(a*b)
    elif op == '/':
        return lambda a, b: IntLiteral(a//b)
    else:
        raise UndefinedTokenError(op)


def _MathOperator(tree, ctx: ParsingContext):
    op = tree.root['value']
    if op == '+':
        return Sum
    elif op == '-':
        return Sub
    elif op == '*':
        return Mul
    elif op == '/':
        return Div
    else:
        raise UndefinedTokenError(op)


def _MathOperation(tree, ctx: ParsingContext):
    [left, op, right] = tree.children
    left_node = visit(left, ctx)
    right_node = visit(right, ctx)
    # Se i nodi sono entrambi interi, si sommano prima della generazione
    if isinstance(left_node, (int, n.IntConstantNode)) and isinstance(right_node, (int, n.IntConstantNode)):
        if isinstance(left_node, n.IntConstantNode):
            left_node = left_node.value
        if isinstance(right_node, n.IntConstantNode):
            right_node = right_node.value
        fun = _MathOptimization(op, ctx)
    else:
        fun = _MathOperator(op, ctx)
    return fun(left_node, right_node)

# Compare


def _ConditionOperation(tree, ctx: ParsingContext):
    left = visit(tree.children[0], ctx)
    operation = visit(tree.children[1], ctx)
    right = visit(tree.children[2], ctx)
    return operation(left, right)


def _ConditionOperator(tree, ctx: ParsingContext):
    symbol = tree.root['value']
    if symbol == '>':
        return MoreThan
    elif symbol == '>=':
        return MoreEqual
    elif symbol == '<':
        return LessThan
    elif symbol == '<=':
        return LessEqual
    elif symbol == '=':
        return Equals
    elif symbol == '<>':
        return NotEquals
    else:
        raise UndefinedTokenError(symbol)

# Enumerable


def _Subscripting(tree, ctx: ParsingContext):
    first, *others = tree.children
    first_arg = Variable(visit(first, ctx))
    indexes_node = others[1]
    indexes_arg = visit(indexes_node, ctx)
    if not isinstance(indexes_arg, list):
        indexes_arg = [indexes_arg]
    return Subscripting(first_arg, indexes_arg)

# Controls


def _While(tree, ctx: ParsingContext):
    children = remove_returns(tree.children)
    condition = children[1]
    expr = children[2]
    condition_tree = visit(condition, ctx)
    expr_tree = visit(expr, ctx)
    if len(expr_tree) == 0:
        expr_tree = Nothing()
    elif len(expr_tree) > 1:
        expr_tree = Block(*expr_tree)
    else:
        expr_tree = expr_tree[0]
    return While(condition_tree, expr_tree)


def _Until(tree, ctx: ParsingContext):
    children = remove_returns(tree.children)
    condition = children[1]
    expr = children[2]
    condition_tree = visit(condition, ctx)
    expr_tree = visit(expr, ctx)
    if len(expr_tree) == 0:
        expr_tree = Nothing()
    elif len(expr_tree) > 1:
        expr_tree = Block(*expr_tree)
    else:
        expr_tree = expr_tree[0]
    return Until(condition_tree, expr_tree)


def _If(tree, ctx: ParsingContext):
    children = remove_returns(tree.children)
    condition_tree = children[1]
    expr_tree = children[2]
    else_tree = children[3] if is_rule(
        children[3], else_rule) else None

    expr_ast = visit(expr_tree, ctx)
    if len(expr_ast) == 0:
        expr_ast = Nothing()
    elif len(expr_ast) > 1:
        expr_ast = Block(*expr_ast)
    else:
        expr_ast = expr_ast[0]
    else_ast = visit(else_tree, ctx) if else_tree is not None else Nothing()
    condition_ast = visit(condition_tree, ctx)
    return If(condition_ast, expr_ast) if else_ast is None else If(condition_ast, expr_ast, else_ast)


def _Else(tree, ctx: ParsingContext):
    children = remove_returns(tree.children)
    expr_tree = children[1]
    expr_ast = visit(expr_tree, ctx)
    if len(expr_ast) == 0:
        expr_ast = Nothing()
    elif len(expr_ast) > 1:
        expr_ast = Block(*expr_ast)
    else:
        expr_ast = expr_ast[0]
    return expr_ast

# Tokens


def _Int(tree, ctx: ParsingContext):
    val = int(tree.root['value'])
    if val > 2147483647 or val < -2147483648:
        raise IntSizeError(val)
    return IntLiteral(val)


def _String(tree, ctx: ParsingContext):
    val = tree.root['value'][1:-1]
    if len(val) > 255:
        raise StringSizeError(val)
    return StringLiteral(val)
