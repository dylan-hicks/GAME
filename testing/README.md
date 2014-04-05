###Testing Guide
---
####To Run:

    python test.py

####Result:

Will show which tests failed.

For the matching of compiled target files to correct target files, the compiled target files and the diffs will remain in the _target_ directory only if the test case for that file failed.

####Directory Structure:

source

- Contains source GAME files that are to be compiled

target

- Contains target python files from compilation
- Contains diff files of compiled target python files and the correct target python files

correct

- Contains correct target python files from compilation

####Pending:

- Actual test cases for the the compiler
- Test Discovery (need other tests first)
- Testing of parser (token stream) and more modular compiler tests using unittest assertions
