from abc import ABC, abstractmethod
from typing import List
from tinyhi.generation.context import Context
from llvmlite.ir import IRBuilder
from llvmlite import ir
import tinyhi.generation.layout as layout
import tinyhi.generation.functions as fn
from .error import *


class ASTNode(ABC):
    @abstractmethod
    def codegen(self, builder: IRBuilder, ctx: Context):
        pass


class ExpressionNode(ASTNode):
    def __init__(self):
        self.children: List[ASTNode] = []

    def check_children(self):
        if len(self.children) not in self.expected_children():
            raise ChildrenNumberError(
                len(self.children), self.expected_children(), type(self))

    @abstractmethod
    def expected_children(self) -> list:
        return [len(self.children)]


class ProgramNode(ExpressionNode):
    def __init__(self):
        super().__init__()

    def codegen(self, builder: IRBuilder, ctx: Context):
        for child in self.children:
            child.codegen(builder, ctx)

    def entry_point(self):
        if len(self.children) > 0:
            return self.children[-1].name
        else:
            raise EntryPointError()

    def expected_children(self):
        return super().expected_children()

# Functions


class FunctionDefinitionNode(ExpressionNode):
    def __init__(self, name, args):
        super().__init__()
        self.name = name
        self.args = args

    def codegen(self, builder: IRBuilder, ctx: Context):
        fnTy = ir.FunctionType(layout.ObjectPtrType(), [
                               layout.ObjectPtrType() for arg in self.args])
        fun = ir.Function(ctx.module, fnTy, name=self.name)
        ctx.parameters = dict(zip(self.args, fun.args))
        ctx.start_function(fun)

        top = fun.append_basic_block()
        builder.position_at_end(top)
        ctx.label = top
        for child in self.children:
            child.codegen(builder, ctx)

        ctx.end_function()

    def expected_children(self):
        return super().expected_children()


class FunctionCallNode(ExpressionNode):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def codegen(self, builder: IRBuilder, ctx: Context):
        self.check_children()

        fun = ctx.get_function(self.name)
        if fun is None:
            raise FunctionNotFoundError(self.name)

        arguments = []
        for child in self.children:
            arguments.append(child.codegen(builder, ctx))
        return builder.call(fun, arguments)

    def expected_children(self):
        return super().expected_children()


class BlockNode(ExpressionNode):
    def __init__(self):
        super().__init__()

    def codegen(self, builder: IRBuilder, ctx: Context):
        last = None
        for child in self.children:
            last = child.codegen(builder, ctx)
        return last

    def expected_children(self):
        return super().expected_children()


class ReturnNode(ExpressionNode):
    def __init__(self):
        super().__init__()

    def expected_children(self):
        return [1]

    def codegen(self, builder: IRBuilder, ctx: Context):
        ptr = self.children[0].codegen(builder, ctx)
        if ptr is None:
            ReturnError()
        # La funzione crea una copia, la registra ad un livello inferiore e la restituisce
        fun = ctx.get_function(fn.return_and_collect_function)
        new_ptr = builder.call(fun, [ptr])
        return builder.ret(new_ptr)


class ReturnVoidNode(ASTNode):
    def __init__(self):
        super().__init__()

    def codegen(self, builder: IRBuilder, ctx: Context):
        return builder.ret_void()

# Variables


class ReferenceNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def codegen(self, builder: IRBuilder, ctx: Context):
        if ctx.is_global(self.name):
            if ctx.global_exists(self.name):
                gv = ctx.get_global(self.name)
                # Se e' globale e gia' esiste, carico l'oggetto dall'indirizzo della globale
                return builder.load(gv)
            else:
                gv = ir.GlobalVariable(
                    ctx.module, layout.ObjectPtrType(), self.name)
                gv.linkage = "internal"
                address = builder.call(
                    ctx.get_function(fn.alloc_global_function), [])
                builder.store(address, gv)
                ctx.set_global(self.name, gv)
                # Se e' globale ma non esiste, la creo A = object**, alloco un B = object, ne prendo l'indirizzo e lo salvo dentro (*B = &A)
                return address
        else:
            var = ctx.get_variable(self.name)
            if var is None:
                raise UnknownVariableError(self.name)
            return var

# Constants

### ABSTRACT ###


class ConstantNode(ASTNode):
    def __init__(self, value):
        super().__init__()
        self.value = value


class IntConstantNode(ConstantNode):
    def __init__(self, value: int):
        super().__init__(value)

    def codegen(self, builder: IRBuilder, ctx: Context):
        return ir.Constant(ir.IntType(32), self.value)


class StringConstantNode(ConstantNode):
    def __init__(self, value):
        super().__init__(value)

    def codegen(self, builder: IRBuilder, ctx: Context):
        ptr = builder.alloca(ir.ArrayType(ir.IntType(8), len(self.value) + 1))
        mapped = list(map(lambda x: ir.Constant(
            ir.IntType(8), ord(x)), list(self.value)))  # La trasformo in un array di char
        mapped.append(ir.Constant(
            ir.IntType(8), 0))  # Aggiungo il terminatore
        value = ir.Constant.literal_array(mapped)

        builder.store(value, ptr)
        return builder.bitcast(ptr, ir.PointerType(ir.IntType(8)))


class AllocIntNode(FunctionCallNode):
    def __init__(self) -> None:
        super().__init__(fn.assign_int_function)


class AllocStringNode(FunctionCallNode):
    def __init__(self) -> None:
        super().__init__(fn.assign_string_function)


class AllocVectorNode(FunctionCallNode):
    def __init__(self) -> None:
        super().__init__(fn.assign_concatenation_function)


class AssignmentNode(ExpressionNode):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def expected_children(self):
        return [0, 1]

    def codegen(self, builder: IRBuilder, ctx: Context):
        self.check_children()
        if len(self.children) == 0:
            return  # Da vedere se fare un collect manuale

        value = self.children[0].codegen(builder, ctx)

        if ctx.is_global(self.name):
            dest = None
            if ctx.global_exists(self.name):
                gv = ctx.get_global(self.name)
                dest = builder.load(gv)
            else:
                # Se e' globale e non esiste, la creo su LLVM, poi la assegno un valore creato con alloc_global
                gv = ir.GlobalVariable(
                    ctx.module, layout.ObjectPtrType(), self.name)
                gv.linkage = "internal"
                address = builder.call(
                    ctx.get_function(fn.alloc_global_function), [])
                ctx.set_global(self.name, gv)
                builder.store(address, gv)
                dest = address
            f = ctx.get_function(fn.copy_function)
            builder.call(f, [value, dest])
        elif not ctx.variable_exists(self.name):
            dest = None
            if isinstance(self.children[0], ReferenceNode):
                f = ctx.get_function(fn.assign_object_function)
                dest = builder.call(f, [value])
            else:
                dest = value
            ctx.set_variable(self.name, dest)
        else:
            if ctx.is_parameter(self.name):
                raise ParameterReferenceError(self.name)
            dest = ctx.get_variable(self.name)
            f = ctx.get_function(fn.copy_function)
            builder.call(f, [value, dest])


class ActivateNode(FunctionCallNode):
    def __init__(self) -> None:
        super().__init__(fn.activate_function)


class CollectNode(FunctionCallNode):
    def __init__(self) -> None:
        super().__init__(fn.collect_function)


class CollectGlobalsNode(FunctionCallNode):
    def __init__(self) -> None:
        super().__init__(fn.collect_globals_function)

# Operations


class BinaryMathNode(FunctionCallNode):
    def __init__(self, name):
        super().__init__(name)

    def expected_children(self):
        return [2]


class BinaryCompareNode(FunctionCallNode):
    def __init__(self, name: str):
        super().__init__(name)

    def expected_children(self):
        return [2]


class LessEqualNode(BinaryCompareNode):
    def __init__(self):
        super().__init__(fn.leq_function)


class LessThanNode(BinaryCompareNode):
    def __init__(self):
        super().__init__(fn.lt_function)


class MoreEqualNode(BinaryCompareNode):
    def __init__(self):
        super().__init__(fn.meq_function)


class MoreThanNode(BinaryCompareNode):
    def __init__(self):
        super().__init__(fn.mt_function)


class EqualsNode(BinaryCompareNode):
    def __init__(self):
        super().__init__(fn.eq_function)


class NotEqualsNode(BinaryCompareNode):
    def __init__(self):
        super().__init__(fn.neq_function)


class SumNode(BinaryMathNode):
    def __init__(self):
        super().__init__(fn.sum_function)


class SubNode(BinaryMathNode):
    def __init__(self):
        super().__init__(fn.sub_function)


class MulNode(BinaryMathNode):
    def __init__(self):
        super().__init__(fn.mul_function)


class DivNode(BinaryMathNode):
    def __init__(self):
        super().__init__(fn.div_function)


class UnaryOperatorNode(FunctionCallNode):
    def __init__(self, name):
        super().__init__(name)

    def expected_children(self):
        return [1]


class NegationNode(UnaryOperatorNode):
    def __init__(self):
        super().__init__(fn.negation_function)


class LengthNode(UnaryOperatorNode):
    def __init__(self):
        super().__init__(fn.length_function)


class SubscriptingNode(FunctionCallNode):
    def __init__(self):
        super().__init__(fn.subscribe_function)

    def codegen(self, builder: IRBuilder, ctx: Context):
        # Check args
        return super().codegen(builder, ctx)

    def expected_children(self):
        return super().expected_children()

    # I/O


class InputNode(FunctionCallNode):
    def __init__(self):
        super().__init__(fn.input_function)

    def expected_children(self):
        return [0]


class OutputNode(FunctionCallNode):
    def __init__(self):
        super().__init__(fn.output_function)

    def expected_children(self):
        return [1]

# Control Flow


class IfNode(ExpressionNode):
    def __init__(self):
        super().__init__()

    def codegen(self, builder: IRBuilder, ctx: Context):
        self.check_children()

        l = len(self.children)

        condition = ctx.function.append_basic_block()
        true = ctx.function.append_basic_block()
        false = None
        if l == 3:
            false = ctx.function.append_basic_block()
        end = ctx.function.append_basic_block()
        if false is None:
            false = end

        builder.branch(condition)
        builder.position_at_end(condition)
        condition_node = self.children[0]
        last = condition_node.codegen(builder, ctx)
        cond_res = builder.icmp_unsigned(
            "!=", last, ir.Constant(ir.IntType(8), 0))
        builder.cbranch(cond_res, true, false)

        ctx.start_scope()

        builder.position_at_end(true)
        ctx.label = true
        true_node = self.children[1]
        true_node.codegen(builder, ctx)
        builder.branch(end)

        ctx.end_scope()

        if l == 3:
            ctx.start_scope()

            builder.position_at_end(false)
            ctx.label = false
            false_node = self.children[2]
            false_node.codegen(builder, ctx)
            builder.branch(end)

            ctx.end_scope()

        builder.position_at_end(end)
        ctx.label = end
        # Alla fine faccio il collect
        collect_fun = ctx.get_function(fn.collect_function)
        builder.call(collect_fun, [])

    def expected_children(self):
        return [2, 3]


class WhileNode(ExpressionNode):
    def __init__(self):
        super().__init__()

    def codegen(self, builder: IRBuilder, ctx: Context):
        self.check_children()

        condition = ctx.function.append_basic_block()
        body = ctx.function.append_basic_block()
        end = ctx.function.append_basic_block()

        builder.branch(condition)
        builder.position_at_end(condition)
        ctx.label = condition
        condition_node = self.children[0]
        last = condition_node.codegen(builder, ctx)
        cond_res = builder.icmp_unsigned(
            "!=", last, ir.Constant(ir.IntType(8), 0))
        builder.cbranch(cond_res, body, end)

        ctx.start_scope()

        builder.position_at_end(body)
        ctx.label = body
        body_node = self.children[1]
        body_node.codegen(builder, ctx)
        # Alla fine faccio il collect
        collect_fun = ctx.get_function(fn.collect_function)
        builder.call(collect_fun, [])
        builder.branch(condition)

        ctx.end_scope()

        builder.position_at_end(end)
        ctx.label = end

    def expected_children(self):
        return [2]


class UntilNode(ExpressionNode):
    def __init__(self):
        super().__init__()

    def codegen(self, builder: IRBuilder, ctx: Context):
        self.check_children()

        body = ctx.function.append_basic_block()
        condition = ctx.function.append_basic_block()
        end = ctx.function.append_basic_block()

        ctx.start_scope()

        builder.branch(body)
        builder.position_at_end(body)
        ctx.label = body
        body_node = self.children[1]
        body_node.codegen(builder, ctx)
        # Alla fine faccio il collect
        collect_fun = ctx.get_function(fn.collect_function)
        builder.call(collect_fun, [])
        builder.branch(condition)

        ctx.end_scope()

        builder.position_at_end(condition)
        ctx.label = condition
        condition_node = self.children[0]
        last = condition_node.codegen(builder, ctx)
        cond_res = builder.icmp_unsigned(
            "!=", last, ir.Constant(ir.IntType(8), 0))
        builder.cbranch(cond_res, body, end)

        builder.position_at_end(end)
        ctx.label = end

    def expected_children(self):
        return [2]
