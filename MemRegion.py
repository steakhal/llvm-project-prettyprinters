import gdb
import pdb
import sys


def create_memregion_printer_for(val):
  CurrentModule = sys.modules[__name__]
  DynamicTypeName = val.dynamic_type.name.rsplit('::', 1)[-1]
  PrinterForDynamicType = getattr(CurrentModule, DynamicTypeName)
  return PrinterForDynamicType(val)


class MemRegion(object):
  def __init__(self, val):
    self.gdbval = val.cast(val.dynamic_type)
    self.Kind = self.gdbval['kind']
    self.static_type = self.gdbval.type
    self.dynamic_type = self.gdbval.dynamic_type

  def display_hint(self):
    return self.static_type.name


class CodeSpaceRegion(MemRegion):
  def __init__(self, val):
    MemRegion.__init__(self, val)

  def to_string(self):
    return "<CodeSpaceRegion printer>"


class GlobalImmutableSpaceRegion(MemRegion):
  def __init__(self, val):
    MemRegion.__init__(self, val)

  def to_string(self):
    return "<GlobalImmutableSpaceRegion printer>"


class GlobalInternalSpaceRegion(MemRegion):
  def __init__(self, val):
    MemRegion.__init__(self, val)

  def to_string(self):
    return "<GlobalInternalSpaceRegion printer>"


class GlobalSystemSpaceRegion(MemRegion):
  def __init__(self, val):
    MemRegion.__init__(self, val)

  def to_string(self):
    return "<GlobalSystemSpaceRegion printer>"


class StaticGlobalSpaceRegion(MemRegion):
  def __init__(self, val):
    MemRegion.__init__(self, val)

  def to_string(self):
    return "<StaticGlobalSpaceRegion printer>"


class HeapSpaceRegion(MemRegion):
  def __init__(self, val):
    MemRegion.__init__(self, val)

  def to_string(self):
    return "<HeapSpaceRegion printer>"


class StackArgumentsSpaceRegion(MemRegion):
  def __init__(self, val):
    MemRegion.__init__(self, val)

  def to_string(self):
    return "<StackArgumentsSpaceRegion printer>"


class StackLocalsSpaceRegion(MemRegion):
  def __init__(self, val):
    MemRegion.__init__(self, val)

  def to_string(self):
    return "<StackLocalsSpaceRegion printer>"


class UnknownSpaceRegion(MemRegion):
  def __init__(self, val):
    MemRegion.__init__(self, val)

  def to_string(self):
    return "<UnknownSpaceRegion printer>"


class AllocaRegion(MemRegion):
  def __init__(self, val):
    MemRegion.__init__(self, val)

  def to_string(self):
    return "<AllocaRegion printer>"


class SymbolicRegion(MemRegion):
  def __init__(self, val):
    MemRegion.__init__(self, val)
    self.Symbol = self.gdbval['sym']

  def to_string(self):
    return 'SymRegion{%s}' % str(self.Symbol.dereference())


class BlockDataRegion(MemRegion):
  def __init__(self, val):
    MemRegion.__init__(self, val)

  def to_string(self):
    return "<BlockDataRegion printer>"


class BlockCodeRegion(MemRegion):
  def __init__(self, val):
    MemRegion.__init__(self, val)

  def to_string(self):
    return "<BlockCodeRegion printer>"


class FunctionCodeRegion(MemRegion):
  def __init__(self, val):
    MemRegion.__init__(self, val)

  def to_string(self):
    return "<FunctionCodeRegion printer>"


class CompoundLiteralRegion(MemRegion):
  def __init__(self, val):
    MemRegion.__init__(self, val)

  def to_string(self):
    return "<CompoundLiteralRegion printer>"


class CXXBaseObjectRegion(MemRegion):
  def __init__(self, val):
    MemRegion.__init__(self, val)

  def to_string(self):
    return "<CXXBaseObjectRegion printer>"


class CXXDerivedObjectRegion(MemRegion):
  def __init__(self, val):
    MemRegion.__init__(self, val)

  def to_string(self):
    return "<CXXDerivedObjectRegion printer>"


class CXXTempObjectRegion(MemRegion):
  def __init__(self, val):
    MemRegion.__init__(self, val)

  def to_string(self):
    return "<CXXTempObjectRegion printer>"


class CXXThisRegion(MemRegion):
  def __init__(self, val):
    MemRegion.__init__(self, val)

  def to_string(self):
    return "<CXXThisRegion printer>"


class FieldRegion(MemRegion):
  def __init__(self, val):
    MemRegion.__init__(self, val)

  def to_string(self):
    return "<FieldRegion printer>"


class ObjCIvarRegion(MemRegion):
  def __init__(self, val):
    MemRegion.__init__(self, val)

  def to_string(self):
    return "<ObjCIvarRegion printer>"


class NonParamVarRegion(MemRegion):
  def __init__(self, val):
    MemRegion.__init__(self, val)
    self.VarDecl = self.gdbval['VD'];

  def to_string(self):
    # FIXME: Implement a pretty printer for clang::NamedDecl.
    # FIXME: Implement accoding to the C++ version.
    VarDeclStr = 'varname' # str(self.VarDecl.dereference())
    return VarDeclStr


class ParamVarRegion(MemRegion):
  def __init__(self, val):
    MemRegion.__init__(self, val)

  def to_string(self):
    return "<ParamVarRegion printer>"


class ElementRegion(MemRegion):
  def __init__(self, val):
    MemRegion.__init__(self, val)
    self.SuperRegion = self.gdbval['superRegion']
    self.ElementType = self.gdbval['ElementType']
    self.Index = self.gdbval['Index']

  def to_string(self):
    # FIXME: Implement a pretty printer for clang::QualType.
    SuperStr = str(self.SuperRegion.dereference())
    IndexStr = str(self.Index)
    TypeStr = 'type' # str(self.ElementType)
    return "Element{%s,%s,%s}" % (SuperStr, IndexStr, TypeStr)


class ObjCStringRegion(MemRegion):
  def __init__(self, val):
    MemRegion.__init__(self, val)

  def to_string(self):
    return "<ObjCStringRegion printer>"


class StringRegion(MemRegion):
  def __init__(self, val):
    MemRegion.__init__(self, val)

  def to_string(self):
    return "<StringRegion printer>"



