cmake_minimum_required(VERSION 3.0)
project(example_project LANGUAGES NONE)


add_custom_command(OUTPUT StaticAnalyzerEnums.py
  COMMAND cpp -E -o StaticAnalyzerEnums.py StaticAnalyzerEnums.py.def
  DEPENDS "Regions.def Symbols.def SVals.def"
  COMMENT "Generating StaticAnalyzerEnums.py for gdb pretty printers"
  VERBATIM
)

add_custom_target(generate DEPENDS StaticAnalyzerEnums.py)

