import llvmlite.ir as ir
import tinyhi.generation.layout as layout

# Unary

negation_function = "negate"
length_function = "length"


def negation(module):
    return ir.Function(module, ir.FunctionType(layout.ObjectPtrType(), [layout.ObjectPtrType()]), negation_function)


def length(module):
    return ir.Function(module, ir.FunctionType(layout.ObjectPtrType(), [layout.ObjectPtrType()]), length_function)

# Assign


assign_object_function = "assign_object"
assign_int_function = "assign_int"
assign_string_function = "assign_string"
assign_concatenation_function = "assign_concatenation"
assign_empty_function = 'assign_empty'


def assign_object(module):
    return ir.Function(module, ir.FunctionType(layout.ObjectPtrType(), [layout.ObjectPtrType()]), assign_object_function)


def assign_int(module):
    return ir.Function(module, ir.FunctionType(layout.ObjectPtrType(), [ir.IntType(32)]), assign_int_function)


def assign_string(module):
    return ir.Function(module, ir.FunctionType(layout.ObjectPtrType(), [ir.PointerType(ir.IntType(8))]), assign_string_function)


def assign_concatenation(module):
    return ir.Function(module, ir.FunctionType(layout.ObjectPtrType(), [ir.IntType(32)], var_arg=True), assign_concatenation_function)


def assign_empty(module):
    return ir.Function(module, ir.FunctionType(layout.ObjectPtrType(), []), assign_empty_function)

# Memory


activate_function = "activate"
collect_function = "collect"
copy_function = "copy"
return_and_collect_function = "return_and_collect"
alloc_global_function = "alloc_global"
collect_globals_function = "collect_globals"


def activate(module):
    return ir.Function(module, ir.FunctionType(ir.VoidType(), []), activate_function)


def collect(module):
    return ir.Function(module, ir.FunctionType(ir.VoidType(), []), collect_function)


def copy(module):
    return ir.Function(module, ir.FunctionType(ir.VoidType(), [layout.ObjectPtrType(), layout.ObjectPtrType()]), copy_function)


def return_and_collect(module):
    return ir.Function(module, ir.FunctionType(layout.ObjectPtrType(), [layout.ObjectPtrType()]), return_and_collect_function)


def alloc_global(module):
    return ir.Function(module, ir.FunctionType(layout.ObjectPtrType(), []), alloc_global_function)


def collect_globals(module):
    return ir.Function(module, ir.FunctionType(ir.VoidType(), []), collect_globals_function)

# I/O


input_function = "input"
output_function = "output"


def base_input(module):
    return ir.Function(module, ir.FunctionType(layout.ObjectPtrType(), []), input_function)


def base_output(module):
    return ir.Function(module, ir.FunctionType(ir.VoidType(), [layout.ObjectPtrType()]), output_function)

# Comparison


lt_function = "lt"
leq_function = "leq"
mt_function = "mt"
meq_function = "meq"
eq_function = "eq"
neq_function = "neq"


def eq(module):
    return ir.Function(module, ir.FunctionType(ir.IntType(8), [layout.ObjectPtrType(), layout.ObjectPtrType()]), eq_function)


def neq(module):
    return ir.Function(module, ir.FunctionType(ir.IntType(8), [layout.ObjectPtrType(), layout.ObjectPtrType()]), neq_function)


def lt(module):
    return ir.Function(module, ir.FunctionType(ir.IntType(8), [layout.ObjectPtrType(), layout.ObjectPtrType()]), lt_function)


def leq(module):
    return ir.Function(module, ir.FunctionType(ir.IntType(8), [layout.ObjectPtrType(), layout.ObjectPtrType()]), leq_function)


def mt(module):
    return ir.Function(module, ir.FunctionType(ir.IntType(8), [layout.ObjectPtrType(), layout.ObjectPtrType()]), mt_function)


def meq(module):
    return ir.Function(module, ir.FunctionType(ir.IntType(8), [layout.ObjectPtrType(), layout.ObjectPtrType()]), meq_function)


# Math

sum_function = "sum"
sub_function = "sub"
mul_function = "mul"
div_function = "division"
subscribe_function = "subscribe"


def sum_(module):
    return ir.Function(module, ir.FunctionType(layout.ObjectPtrType(), [layout.ObjectPtrType(), layout.ObjectPtrType()]), sum_function)


def sub_(module):
    return ir.Function(module, ir.FunctionType(layout.ObjectPtrType(), [layout.ObjectPtrType(), layout.ObjectPtrType()]), sub_function)


def mul_(module):
    return ir.Function(module, ir.FunctionType(layout.ObjectPtrType(), [layout.ObjectPtrType(), layout.ObjectPtrType()]), mul_function)


def div_(module):
    return ir.Function(module, ir.FunctionType(layout.ObjectPtrType(), [layout.ObjectPtrType(), layout.ObjectPtrType()]), div_function)


def subscribe(module):
    return ir.Function(module, ir.FunctionType(layout.ObjectPtrType(), [layout.ObjectPtrType(), ir.IntType(32)], var_arg=True), subscribe_function)


class BaseLibrary():
    def __init__(self, module):
        self.module = module
        self.lib = dict()
        self.base_lib = dict()
        self.library_init()

    # Costruisce una dispatch table con tutte le funzioni della standard lib
    def library_init(self):
        # Assign
        self.lib[assign_object_function] = assign_object
        self.lib[assign_int_function] = assign_int
        self.lib[assign_string_function] = assign_string
        self.lib[assign_empty_function] = assign_empty
        self.lib[assign_concatenation_function] = assign_concatenation
        # I/O
        self.lib[output_function] = base_output
        self.lib[input_function] = base_input
        # Memory
        self.lib[activate_function] = activate
        self.lib[collect_function] = collect
        self.lib[copy_function] = copy
        self.lib[return_and_collect_function] = return_and_collect
        self.lib[collect_globals_function] = collect_globals
        self.lib[alloc_global_function] = alloc_global
        # Compare
        self.lib[eq_function] = eq
        self.lib[neq_function] = neq
        self.lib[lt_function] = lt
        self.lib[leq_function] = leq
        self.lib[mt_function] = mt
        self.lib[meq_function] = meq
        # Math
        self.lib[negation_function] = negation
        self.lib[length_function] = length
        self.lib[sum_function] = sum_
        self.lib[sub_function] = sub_
        self.lib[mul_function] = mul_
        self.lib[div_function] = div_
        self.lib[subscribe_function] = subscribe

    def get(self, name: str) -> ir.Function:
        if self.base_lib.get(name) == None:
            fun = self.lib.get(name)
            if fun is None:
                return None
            fun = fun(self.module)
            self.base_lib[name] = fun
            return fun
        else:
            return self.base_lib[name]
