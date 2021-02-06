from functools import cmp_to_key


def function_sort(arg_a, arg_b):
    """
    Ordina le funzioni sulla base della chiave, che e' una tupla di interi rappresentante la posizione nell'albero della funzione
    """
    a = arg_a[0]
    b = arg_b[0]
    if len(a) > len(b):
        return -1
    elif len(b) > len(a):
        return 1
    else:
        l = len(a)
        counter = -1
        while (l + counter) != 0:
            if a[counter] > b[counter]:
                return 1
            elif b[counter] > a[counter]:
                return -1
            else:
                counter -= 1


class ParsingContext():
    def __init__(self):
        self.current_scopes = []
        self.functions = dict()
        self.current_function_name = None

    def start_function(self, level):
        self.current_scopes.append(level)

    def add_function(self, function):
        self.functions[tuple(self.current_scopes)] = function

    def end_function(self):
        self.current_scopes.pop()

    def get_functions(self):
        v = list(self.functions.items())
        v = sorted(v, key=cmp_to_key(function_sort))
        return list(map(lambda x: x[1], v))
