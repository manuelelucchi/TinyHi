import enum
from abc import ABC
from llvmlite import ir
from tinyhi.generation.functions import BaseLibrary
from typing import List, Dict
from .error import *


class Scope():
    def __init__(self):
        self.variables: Dict[str, ir.Value] = dict()


class Context():
    def __init__(self, module: ir.Module):
        self.module = module
        self.function: ir.Function = None
        self.functions: Dict[str, ir.Function] = dict()
        self.parameters = dict()
        self.label = None
        self.globals: Dict[str, ir.GlobalVariable] = dict()
        self.scopes: List[Scope] = []
        self.base_lib = BaseLibrary(self.module)

    def end_function(self):
        self.end_scope()
        self.scopes = []
        self.function = None
        self.parameters = dict()
        self.label = None

    def start_function(self, function: ir.Function):
        self.function = function
        self.functions[function.name] = function
        self.scopes = [Scope()]

    def start_scope(self):
        self.scopes.append(Scope())

    def end_scope(self):
        self.scopes.pop()

    def is_current_variable(self, name: str) -> bool:
        return self.scopes[-1].variables.get(name) is not None

    def get_global(self, name):
        return self.globals.get(name)

    def get_variable(self, name: str):
        var = self.parameters.get(name)  # Is global
        if var != None:
            return var
        var = self.globals.get(name)  # Is parameter
        if var != None:
            return var
        for s in reversed(self.scopes):
            var = s.variables.get(name)
            if var != None:
                return var
        return None

    def set_global(self, name: str, value: ir.Value):
        if self.global_exists(name):
            raise GlobalReferenceError(name)
        else:
            self.globals[name] = value

    def set_variable(self, name: str, value: ir.Value):
        if self.is_parameter(name):
            raise ParameterReferenceError(name)
        if self.global_exists(name):
            raise GlobalReferenceError(name)
        self.scopes[-1].variables[name] = value

    def is_parameter(self, name: str):
        return self.parameters.get(name) is not None

    def is_global(self, name: str):
        return name[0] == '.'

    def global_exists(self, name: str):
        return self.globals.get(name) is not None

    def variable_exists(self, name: str):
        return self.get_variable(name) is not None

    def get_function(self, name: str) -> ir.Function:
        fun = self.base_lib.get(name)
        fun = self.functions.get(name) if fun is None else fun
        return fun
