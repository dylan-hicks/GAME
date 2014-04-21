###User Guide
---

####Initial Setup:

When you are setting up a new GAME directory, if there is no ./gamec executable present, then please run the following command:

    make

You will only need to run this command once for a directory as the ./gamec executable does not need updating.

####To Run:

    ./gamec [.game file]
    python run.py [.game.py file]

####\*.game Operator:

Using the * operator in front of the .game extension allows the compiler to compile all the relevant .game files at once.

    ./gamec *.game

This command will compile all the .game files in the current directory.

    ./gamec temp/*.game

This command will compile all the .game files in the temp directory.

####Moving flag:

Usage of the "_-m_" flag allows the user to specify a directory after the flag that the compiled .game.py files should be moved to after compilation.

    ./gamec *.game -m temp

This command will compile all of the .game files in the current directory and then move them to the temp directory if it exists. If the directory doesn't exist, it will be created and then the compiled files will be moved to it.
