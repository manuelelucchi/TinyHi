from tinyhi.ast import AST
from tinyhi.parsing import Parse
from tinyhi.generation import Codegen
from tinyhi.jit import JIT

try:
    from time import perf_counter as time
except ImportError:
    from time import time


def show_error():
    print("Terminating")


def run(input, log_ir=False, log_time=False, opt_level=2):
    """ Compila ed esegue una stringa di codice TinyHi

    Args:
        input: La stringa di codice.
        log_ir: Un boolean che indica se fare il print dell'IR generato (default `False`).
        log_time: Un boolean che indica se fare il print dei tempi impiegati dalle varia fasi (default `False`).
        opt_level: Il livello di ottimizzazione dell'IR (default 2).
    """
    # Parsing

    start = time()

    tree = Parse(input)
    if tree is None:
        show_error()
        return

    end = time()

    print('Parsing time: {:9.2f} ms'.format(
        (end-start)*1000)) if log_time else None

    # AST

    start = time()

    ast = AST(tree)
    if ast is None:
        show_error()
        return

    end = time()

    print('AST Generation time: {:9.2f} ms'.format(
        (end-start)*1000)) if log_time else None

    # IR

    start = time()

    (llmod, entry) = Codegen(ast, log_ir)
    if llmod is None:
        show_error()
        return

    end = time()

    print('IR Generation time: {:9.2f} ms'.format(
        (end-start)*1000)) if log_time else None

    # Execution

    start = time()

    try:
        JIT(llmod, entry, opt_level)
    except Exception as e:
        print("Execution Failed")
        print("RuntimeError: {}".format(e))
        return

    end = time()
    print('Execution time: {:9.2f} ms'.format(
        (end-start)*1000)) if log_time else None
