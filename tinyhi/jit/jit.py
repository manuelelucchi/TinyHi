from ctypes import CFUNCTYPE, c_int, POINTER
import llvmlite.binding as llvm


def JIT(llmod, entry, opt_level=2):
    """ Funzione che ottimizza, compila just in time ed esegue un LLVM IR

    Args:
        llmod: l'LLVM IR.
        entry: Il nome della funzione di avvio
        opt_level: Il livello di ottimizzazione (default 2)
    """
    if opt_level != None:
        pmb = llvm.create_pass_manager_builder()

        pmb.opt_level = opt_level

        pm = llvm.create_module_pass_manager()
        pmb.populate(pm)

        pm.run(llmod)

    target_machine = llvm.Target.from_default_triple().create_target_machine()

    with llvm.create_mcjit_compiler(llmod, target_machine) as ee:
        ee.finalize_object()
        cfptr = ee.get_function_address(entry)

        # Si presume che la funzione piu' esterna non prenda argomenti e non restituisca valori
        cfunc = CFUNCTYPE(None)(cfptr)
        cfunc()
