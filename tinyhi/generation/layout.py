"""
In questo modulo si trovano le definizioni per i tipi di tiny hi
"""

import llvmlite.ir as ir

__object__ = None

__pointer__ = None


def ObjectType():
    global __object__
    if __object__ is None:
        __object__ = ir.global_context.get_identified_type("tiny_hi_object_s")
        __object__.set_body(ir.IntType(96), ir.IntType(8))
    return __object__


def ObjectPtrType():
    global __pointer__
    if __pointer__ is None:
        __pointer__ = ir.PointerType(ObjectType())
    return __pointer__


def BoolType():
    return ir.IntType(8)
