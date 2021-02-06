class ReturnError(Exception):
    def __init__(self):
        super().__init__("Trying to return an unknown variable")


class AssignValueError(Exception):
    def __init__(self, value, name):
        super().__init__("{} is not a valid value to be assigned to variable {}".format(value, name))


class SubscriptingError(Exception):
    def __init__(self, value, name):
        super().__init__("{} is not a valid value for subscripting variable {}".format(value, name))


class ChildrenNumberError(Exception):
    def __init__(self, number, expected, name):
        super().__init__("Got {} children for the node {}, expected {}".format(
            number, name, expected))


class EntryPointError(Exception):
    def __init__(self):
        super().__init__("Cannot find program entry point")


class FunctionNotFoundError(Exception):
    def __init__(self, name):
        super().__init__("Function {} cannot be found".format(name))


class AssignmentError(Exception):
    def __init__(self):
        super().__init__("Expected at least one children to assign")


class StdlibNotFoundError(Exception):
    def __init__(self):
        super().__init__("Cannot find the stdlib. Check if the binary exists")


class GlobalReferenceError(Exception):
    def __init__(self, name: str) -> None:
        super().__init__("Trying to change the reference to the global variable {}".format(name))


class ParameterReferenceError(Exception):
    def __init__(self, name: str) -> None:
        super().__init__("Trying to modifing the parameter {} is illegal".format(name))


class ConcatenationError(Exception):
    def __init__(self) -> None:
        super().__init__("You can't concatenate strings and int")


class UnknownVariableError(Exception):
    def __init__(self, name) -> None:
        super().__init__("Variable {} has not been previously assigned or declared".format(name))
