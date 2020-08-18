void clang_analyzer_dump(const char*);

void testing(char *src, int idx) {
  clang_analyzer_dump(&src[idx + 2]);
}

