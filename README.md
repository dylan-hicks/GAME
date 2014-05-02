###User Guide
---

####Initial Setup:

When you are setting up a new GAME directory, if there is no ./gamec executable present, then please run the following command:

    make

You will only need to run this command once for a directory as the ./gamec executable does not need updating.

####To Run:

    ./gamec [.game file]
    python [.game.py file]

####Compile Operation Flow:

    When you run the following command:
    
    ./gamec [.game file]

    The compiler sets -m and -o flags for moving and output and then executes

    python include.py [.game file]

    and then creates a .game.temp file that has the include statements removed and the appropriate library code inserted.

    Then, the gamec executable runs

    python game.py [.game.temp file]

    which will run the parser and other compile operations on the .game.temp file and write the resulting python code to a .game.py file.

    The gamec exectuable then cleans up the .game.temp file.
