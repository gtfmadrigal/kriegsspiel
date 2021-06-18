# umpire

This is a Python script for use by the Umpire in managing a game of Kriegsspiel.

Effectively, the script works by importing a gamefile, which creates the particular scenario.

Kriegsspiel is based around a shell, from which the user inputs various commands, like move, search, hide, fire, attack, or torpedo. The shell interprets these commands and alters the gamestate accordingly based on the information provided by the gamefile and the user's input.

The principal game code is held in kriegsspiel.py, and this is where the import statements can be modified when the gamefile is to be changed.

The gamefiles are stored in their own directory, gamefiles/. Every gamefile is named according to the format battle.py, hence "brandywine".py, after the Battle of the Brandywine River, and "nile".py, after the Battle of the Nile. Within the gamefiles/ directory, a file called scenariotemplate.py is included as an example so that the user can make his own gamefile. 

Manual pages explaining the various commands within kriegsspiel.py are contained as plaintext inside the directory manpages/. They can be viewed with an ordinary text editor, or by using the command man (command) within the Kriegsspiel shell.

Kriegsspiel is highly documented, with most of the documentation found in the directory documentation/. Rules for the game itself are contained within Kriegspiel Third Edition.docx (pardon the misspelling). A Fourth Edition is in the works to be supplied once this program reaches a working completion stage, with land, sea, air, space, and technological warfare all integrated together. A non-working educational version of kriegsspiel.py with heavy commentary can be found in documentation/annotated_kriegsspiel.py. The license, changelog, and release notes can also be found within documentation/.