
class IllegalFunctionCallError(Exception):
    def __init__(self, caller_name, called_name):
        super().__init__("You can't call the function {} from the function {}".format(
            called_name, caller_name))


class ASTGenerationError(Exception):
    def __init__(self, node):
        super().__init__("There's been an error while analyzing the following element {}".format(node))


class UndefinedTokenError(Exception):
    def __init__(self, op):
        super().__init__("The token {} does not exist".format(op))


class UndefinedRuleError(Exception):
    def __init__(self, op):
        super().__init__("The token {} does not exist".format(op))


class NotRuleOrTokenError(Exception):
    def __init__(self, t):
        super().__init__("The node is not a rule or token, found {}".format(t))


class IntSizeError(Exception):
    def __init__(self, t: int):
        super().__init__("{} is a value either too big or too small for an integer".format(t))


class StringSizeError(Exception):
    def __init__(self, t: str):
        super().__init__("\"{}\" is too big to be a string literal".format(t))


class NegateError(Exception):
    def __init__(sel) -> None:
        super().__init__("Negating a string is not permitted")
