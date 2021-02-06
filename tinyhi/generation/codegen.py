from tinyhi.generation.nodes import ProgramNode
import llvmlite.binding as llvm
from llvmlite.ir import Module, IRBuilder
from tinyhi.generation.context import Context

import pathlib
import platform


def Codegen(ast: ProgramNode, printIR: bool = True):
    """Genera l'LLVM IR dall'AST in input. 

    Args:
        ast: L'albero di sintassi astratto.
        printIR (bool): Un boolean che indica se fare un print dell'IR generato (default `False`)

    Returns:
        L'IR generato sotto forma di `str`

    Raises:
        StdlibNotFoundError: Se la standard lib non puo' essere trovata
    """

    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    # Decide l'estensione della stdlib
    ext = None
    if platform.system() == 'Windows':
        ext = 'dll'
    elif platform.system() == 'Darwin':
        ext = 'dylib'
    elif platform.system() == 'Linux':
        ext = 'so'

    path = pathlib.Path(__file__).parent.absolute()
    try:
        llvm.load_library_permanently(
            str(path) + "/../../bin/tiny_hi_core.{}".format(ext))
    except Exception:
        print("StdlibNotFoundError: Cannot find the standard library (tiny_hi_core.{})".format(ext))
        return (None, None)

    module = Module()
    builder = IRBuilder()
    context = Context(module)

    entry = None

    llmod = None

    try:
        entry = ast.entry_point()
        ast.codegen(builder, context)

        strmod = str(module)

        if printIR:
            print(strmod)

        llmod = llvm.parse_assembly(strmod)

    except Exception as e:
        print("Codegen Failed")
        print("{}: {}".format(type(e).__name__, e))
    finally:
        return (llmod, entry)
