###Testing Guide
---
####To Run:

    make

- This will remove all temporary files after the test suite has run.

####To Run and persist temporary files:

    make persist

- This will have the temporary files in target, outputs, and diffs persist.

####Result:

Will show which tests failed. The test framework compiles the .game files in the _source_ directory and places the output compiled python files in the _target_ directory. It then runs each compiled python file and places the outputs as a text file into the _output_ directory and then creates a diff between that output text file and its correct counterpart in the _correct_ directory. If the diff file is empty, then that .game file compiled and worked correctly and that test case passes.

After each test script operation with _make persist_, the outputs and the diffs will respectively remain in the _output_ and _diffs_ directory. The compiled python target files will remain in the _target_ directory. Otherwise, no temporary files will remain after running the test suite with _make_. 

####Directory Structure:

_source_

- Contains source GAME files that are to be compiled

_target_

- Contains target python files from compilation

_diffs_

- Contains diff files of compiled target python files and the correct target python files

_correct_

- Contains the correct outputs

####Cleaning Directories:

    make clean

This command cleans the target, output, and diffs directories.

####Pending:

- Actual test cases for the the compiler
