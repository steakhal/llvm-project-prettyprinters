import gdb
import pdb
import sys

from StaticAnalyzerEnums import BaseKind, NonLocKind, LocKind

def create_sval_printer_for(val):
  BaseBits = 2
  BaseMask = 0b11

  Kind = val["Kind"]
  CurrentBaseKind = Kind & BaseMask
  CurrentSubKind = Kind >> BaseBits

  # Delegate to constructor accoding to kind values.
  if CurrentBaseKind == BaseKind.UnknownValKind.value:
    return UnknownVal(val)
  if CurrentBaseKind == BaseKind.UndefinedValKind.value:
    return UndefinedVal(val)

  if CurrentBaseKind == BaseKind.NonLocKind.value:
    if CurrentSubKind == NonLocKind.ConcreteIntKind.value:
      return NonLocConcreteInt(val)
    if CurrentSubKind == NonLocKind.SymbolValKind.value:
      return SymbolVal(val)
    if CurrentSubKind == NonLocKind.LocAsIntegerKind.value:
      return LocAsInteger(val)
    if CurrentSubKind == NonLocKind.CompoundValKind.value:
      return CompoundVal(val)
    if CurrentSubKind == NonLocKind.LazyCompoundValKind.value:
      return LazyCompoundVal(val)
    if CurrentSubKind == NonLocKind.PointerToMemberKind.value:
      return PointerToMember(val)
    assert False, 'Are there other NonLoc?'

  if CurrentBaseKind == BaseKind.LocKind.value:
    if CurrentSubKind == LocKind.ConcreteIntKind.value:
      return LocConcreteInt(val)
    if CurrentSubKind == LocKind.GotoLabelKind.value:
      return GotoLabel(val)
    if CurrentSubKind == LocKind.MemRegionValKind.value:
      return MemRegionVal(val)
    assert False, 'Are there other Loc?'
  assert False, 'Are there other BaseKind?'


class SVal(object):
  def __init__(self, val):
    self.gdbval = val.cast(val.dynamic_type)
    self.Data = self.gdbval["Data"]
    self.static_type = self.gdbval.type
    self.dynamic_type = self.gdbval.dynamic_type

  def display_hint(self):
    return self.static_type.name

  def to_string(self):
    assert False, 'Only a derived class of SVal should be printed.'


# Unknown and Undefined printers
class UnknownVal(SVal):
  def __init__(self, val):
    SVal.__init__(self, val)

  def to_string(self):
    return 'Unknown'

class UndefinedVal(SVal):
  def __init__(self, val):
    SVal.__init__(self, val)

  def to_string(self):
    return 'Undefined'


# NonLoc printers
class NonLocConcreteInt(SVal):
  def __init__(self, val):
    SVal.__init__(self, val)
    APSIntPtrTy = gdb.lookup_type('llvm::APSInt').const().pointer()
    self.Integer = self.Data.cast(APSIntPtrTy)

  def to_string(self):
    # FIXME: Implement according to the C++ version.
    return str(self.Integer.dereference())


class SymbolVal(SVal):
  def __init__(self, val):
    SVal.__init__(self, val)
    MemRegionPtrTy = gdb.lookup_type('clang::ento::SymExpr').const().pointer()
    self.Symbol = self.Data.cast(MemRegionPtrTy)

  def to_string(self):
    return str(self.Symbol.dereference())


class LocAsInteger(SVal):
  def __init__(self, val):
    SVal.__init__(self, val)

  def to_string(self):
    return '<LocAsInteger printer>'


class CompoundVal(SVal):
  def __init__(self, val):
    SVal.__init__(self, val)

  def to_string(self):
    return '<CompoundVal printer>'


class LazyCompoundVal(SVal):
  def __init__(self, val):
    SVal.__init__(self, val)

  def to_string(self):
    return '<LazyCompoundVal printer>'


class PointerToMember(SVal):
  def __init__(self, val):
    SVal.__init__(self, val)

  def to_string(self):
    return '<PointerToMember printer>'


# Loc printers
class LocConcreteInt(SVal):
  def __init__(self, val):
    SVal.__init__(self, val)
    APSIntPtrTy = gdb.lookup_type('llvm::APSInt').const().pointer()
    self.Integer = self.Data.cast(APSIntPtrTy)

  def to_string(self):
    # FIXME: Implement.
    IntValue = str(self.Integer.dereference())
    return '%s (loc)' % IntValue


class GotoLabel(SVal):
  def __init__(self, val):
    SVal.__init__(self, val)

  def to_string(self):
    # FIXME: Implement.
    GotoLabelName = 'GotoLabel'
    return '&&%s' % GotoLabelName


class MemRegionVal(SVal):
  def __init__(self, val):
    SVal.__init__(self, val)
    MemRegionPtrTy = gdb.lookup_type('clang::ento::MemRegion').const().pointer()
    self.Region = self.Data.cast(MemRegionPtrTy)

  def to_string(self):
    return '&%s' % str(self.Region.dereference())



