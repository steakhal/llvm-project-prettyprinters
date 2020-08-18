import gdb
import pdb

import sys
sys.path.append('/home/elnbbea/git/prettyprinters')

from SVals import create_sval_printer_for
from SymExpr import create_symexpr_printer_for
from MemRegion import create_memregion_printer_for


class StaticAnalyzerPrettyPrinter(object):
    """PrettyPrinter object so gdb-commands like 'info pretty-printers' work."""

    def __init__(self, name):
        super(StaticAnalyzerPrettyPrinter, self).__init__()
        self.name = name
        self.enabled = True

        self.lookup = {
            "clang::ento::SVal": create_sval_printer_for,
            "clang::ento::Loc": create_sval_printer_for,
            "clang::ento::NonLoc": create_sval_printer_for,
            "clang::ento::UndefinedVal": create_sval_printer_for,
            "clang::ento::DefinedOrUnknownSVal": create_sval_printer_for,
            "clang::ento::UnknownVal": create_sval_printer_for,
            "clang::ento::DefinedSVal": create_sval_printer_for,
            "clang::ento::ConcreteInt": create_sval_printer_for,
            "clang::ento::GotoLabel": create_sval_printer_for,
            "clang::ento::MemRegionVal": create_sval_printer_for,
            "clang::ento::CompoundVal": create_sval_printer_for,
            "clang::ento::ConcreteInt": create_sval_printer_for,
            "clang::ento::LazyCompoundVal": create_sval_printer_for,
            "clang::ento::LocAsInteger": create_sval_printer_for,
            "clang::ento::SymbolVal": create_sval_printer_for,
            "clang::ento::PointerToMember": create_sval_printer_for,

            "clang::ento::SymExpr": create_symexpr_printer_for,
            "clang::ento::BinarySymExpr": create_symexpr_printer_for,
            "clang::ento::IntSymExpr": create_symexpr_printer_for,
            "clang::ento::SymIntExpr": create_symexpr_printer_for,
            "clang::ento::SymSymExpr": create_symexpr_printer_for,
            "clang::ento::SymbolCast": create_symexpr_printer_for,
            "clang::ento::SymbolData": create_symexpr_printer_for,
            "clang::ento::SymbolConjured": create_symexpr_printer_for,
            "clang::ento::SymbolDerived": create_symexpr_printer_for,
            "clang::ento::SymbolExtent": create_symexpr_printer_for,
            "clang::ento::SymbolMetadata": create_symexpr_printer_for,
            "clang::ento::SymbolRegionValue": create_symexpr_printer_for,

            "clang::ento::MemRegion": create_memregion_printer_for,
            "clang::ento::MemSpaceRegion": create_memregion_printer_for,
            "clang::ento::CodeSpaceRegion": create_memregion_printer_for,
            "clang::ento::GlobalsSpaceRegion": create_memregion_printer_for,
            "clang::ento::NonStaticGlobalSpaceRegion": create_memregion_printer_for,
            "clang::ento::GlobalImmutableSpaceRegion": create_memregion_printer_for,
            "clang::ento::GlobalInternalSpaceRegion": create_memregion_printer_for,
            "clang::ento::GlobalSystemSpaceRegion": create_memregion_printer_for,
            "clang::ento::StaticGlobalSpaceRegion": create_memregion_printer_for,
            "clang::ento::HeapSpaceRegion": create_memregion_printer_for,
            "clang::ento::StackSpaceRegion": create_memregion_printer_for,
            "clang::ento::StackArgumentsSpaceRegion": create_memregion_printer_for,
            "clang::ento::StackLocalsSpaceRegion": create_memregion_printer_for,
            "clang::ento::UnknownSpaceRegion": create_memregion_printer_for,
            "clang::ento::SubRegion": create_memregion_printer_for,
            "clang::ento::AllocaRegion": create_memregion_printer_for,
            "clang::ento::SymbolicRegion": create_memregion_printer_for,
            "clang::ento::TypedRegion": create_memregion_printer_for,
            "clang::ento::BlockDataRegion": create_memregion_printer_for,
            "clang::ento::CodeTextRegion": create_memregion_printer_for,
            "clang::ento::BlockCodeRegion": create_memregion_printer_for,
            "clang::ento::FunctionCodeRegion": create_memregion_printer_for,
            "clang::ento::TypedValueRegion": create_memregion_printer_for,
            "clang::ento::CompoundLiteralRegion": create_memregion_printer_for,
            "clang::ento::CXXBaseObjectRegion": create_memregion_printer_for,
            "clang::ento::CXXDerivedObjectRegion": create_memregion_printer_for,
            "clang::ento::CXXTempObjectRegion": create_memregion_printer_for,
            "clang::ento::CXXThisRegion": create_memregion_printer_for,
            "clang::ento::DeclRegion": create_memregion_printer_for,
            "clang::ento::FieldRegion": create_memregion_printer_for,
            "clang::ento::ObjCIvarRegion": create_memregion_printer_for,
            "clang::ento::VarRegion": create_memregion_printer_for,
            "clang::ento::NonParamVarRegion": create_memregion_printer_for,
            "clang::ento::ParamVarRegion": create_memregion_printer_for,
            "clang::ento::ElementRegion": create_memregion_printer_for,
            "clang::ento::ObjCStringRegion": create_memregion_printer_for,
            "clang::ento::StringRegion": create_memregion_printer_for,
        }

        self.subprinters = []
        for name, subprinter in self.lookup.items():
            # Subprinters and names are used only for the rarely used command "info
            # pretty" (and related), so the name of the first data structure it prints
            # is a reasonable choice.
            if subprinter not in self.subprinters:
                subprinter.name = name
                self.subprinters.append(subprinter)

    def __call__(self, val):
        """Return the pretty printer for a val, if the type is supported."""

        # Do not handle any type that is not a struct/class.
        if val.type.strip_typedefs().code != gdb.TYPE_CODE_STRUCT:
            return None

        # Handle any using declarations or other typedefs.
        # TODO: typename = _prettify_typename(val.type)
        handler = self.lookup.get(val.type.unqualified().name, None)
        if handler:
          #print('Calling handler for ' + val.type.unqualified().name)
          return handler(val)
        return None


_static_analyzer_printer_name = "static_analyzer_printer_name"





def reload_printer():
    for printer in gdb.pretty_printers:
        if getattr(printer, "name", "none") == _static_analyzer_printer_name:
            gdb.pretty_printers.remove(printer)
            break
    gdb.printing.register_pretty_printer(gdb.current_objfile(), StaticAnalyzerPrettyPrinter(_static_analyzer_printer_name))

reload_printer()


