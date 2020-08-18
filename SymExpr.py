import gdb
import pdb
import sys

from StaticAnalyzerEnums import SymKind


def create_symexpr_printer_for(val):
  Kind = val['K']
  # Delegate to constructor accoding to kind values.
  if Kind == SymKind.IntSymExprKind.value:
    return IntSymExpr(val)
  if Kind == SymKind.SymIntExprKind.value:
    return SymIntExpr(val)
  if Kind == SymKind.SymSymExprKind.value:
    return SymSymExpr(val)
  if Kind == SymKind.SymbolCastKind.value:
    return SymbolCast(val)
  if Kind == SymKind.SymbolConjuredKind.value:
    return SymbolConjured(val)
  if Kind == SymKind.SymbolDerivedKind.value:
    return SymbolDerived(val)
  if Kind == SymKind.SymbolExtentKind.value:
    return SymbolExtent(val)
  if Kind == SymKind.SymbolMetadataKind.value:
    return SymbolMetadata(val)
  if Kind == SymKind.SymbolRegionValueKind.value:
    return SymbolRegionValue(val)
  assert False, 'Are there any other SymExprs?'


class SymExpr(object):
  def __init__(self, val):
    self.gdbval = val.cast(val.dynamic_type)
    self.Kind = self.gdbval['K']
    self.static_type = self.gdbval.type
    self.dynamic_type = self.gdbval.dynamic_type

  def display_hint(self):
    return self.static_type.name

class BinarySymExpr(SymExpr):
  def __init__(self, val):
    SymExpr.__init__(self, val)
    self.LHS = self.gdbval['LHS']
    self.RHS = self.gdbval['RHS']
    self.Op = self.gdbval['Op']


class IntSymExpr(BinarySymExpr):
  def __init__(self, val):
    BinarySymExpr.__init__(self, val)

  def to_string(self):
    LHSStr = str(self.LHS.referenced_value())
    RHSStr = str(self.RHS.dereference())
    OpStr = str(self.Op)
    return '%s %s (%s)' % (LHSStr, OpStr, RHSStr)

class SymIntExpr(BinarySymExpr):
  def __init__(self, val):
    BinarySymExpr.__init__(self, val)

  def to_string(self):
    LHSStr = str(self.LHS.dereference())
    RHSStr = str(self.RHS.referenced_value())
    OpStr = str(self.Op)
    return '(%s) %s %s' % (LHSStr, OpStr, RHSStr)

class SymSymExpr(BinarySymExpr):
  def __init__(self, val):
    BinarySymExpr.__init__(self, val)

  def to_string(self):
    LHSStr = str(self.LHS.dereference())
    RHSStr = str(self.RHS.dereference())
    OpStr = str(self.Op)
    return '(%s) %s (%s)' % (LHSStr, OpStr, RHSStr)

class SymbolCast(SymExpr):
  def __init__(self, val):
    SymExpr.__init__(self, val)

  def to_string(self):
    return '<SymbolCast printer>'


class SymbolConjured(SymExpr):
  def __init__(self, val):
    SymExpr.__init__(self, val)

  def to_string(self):
    return '<SymbolConjured printer>'


class SymbolDerived(SymExpr):
  def __init__(self, val):
    SymExpr.__init__(self, val)

  def to_string(self):
    return '<SymbolDerived printer>'


class SymbolExtent(SymExpr):
  def __init__(self, val):
    SymExpr.__init__(self, val)

  def to_string(self):
    return '<SymbolExtent printer>'


class SymbolMetadata(SymExpr):
  def __init__(self, val):
    SymExpr.__init__(self, val)

  def to_string(self):
    return '<SymbolMetadata printer>'


class SymbolRegionValue(SymExpr):
  def __init__(self, val):
    SymExpr.__init__(self, val)
    self.Region = self.gdbval['R']
    self.ID = self.gdbval['Sym'].cast(gdb.lookup_type('unsigned'))

  def to_string(self):
    # FIXME: Implement according to the C++ version.
    return 'reg_$%d' % (self.ID) 



