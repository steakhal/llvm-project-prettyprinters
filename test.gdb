set breakpoint pending on
source /home/elnbbea/git/prettyprinters/printer.py

b SVals.cpp:279
commands 1
  del 1
  print *this
end

run -cc1 -internal-isystem lib/clang/12.0.0/include -nostdsysteminc -analyze -analyzer-constraints=range -setup-static-analyzer -analyzer-checker=core,debug.ExprInspection /home/elnbbea/git/prettyprinters/test.c



