from liblet import ANTLR
import pathlib
from io import StringIO
from contextlib import redirect_stdout

import liblet
from .error import *

__parser__ = None


def _Parser():
    global __parser__
    if __parser__ is None:
        p = str(pathlib.Path(__file__).parent.absolute())
        path = p + "/TinyHi.g"
        f = open(path)
        txt = f.read()
        __parser__ = ANTLR(txt)
    return __parser__


def Parse(input):
    """Genera l'albero di parsing dell'input dato secondo le regole della grammatica.

    Args:
        input :obj:`str`: Il programma in input

    Raises:
        ParserError: se il programma non rispetta le regole della grammatica
    """

    if input is None or input == "":
        print("Parse Failed")
        print("Input can't be null or empty")
        return None
    p = _Parser()
    tree = p.tree(input, 'program')
    if tree is None:
        print("Parse Failed")
        print("Parsing can't be completed")
        return None
    return tree
