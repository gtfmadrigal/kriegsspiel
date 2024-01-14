# umpire

This is a Python script for use by the Umpire in managing a game of Eschaton.

Effectively, the script works by importing a gamefile, which creates the particular scenario.

Eschaton is based around a shell, from which the user inputs various commands, like move, search, hide, fire, attack, or torpedo. The shell interprets these commands and alters the gamestate accordingly based on the information provided by the gamefile and the user's input.

The principal game code is held in umpire.py, and this is where the import statements can be modified when the gamefile is to be changed.

The gamefiles are stored in their own directory, gamefiles/. Every gamefile is named according to the format battle.py, hence "brandywine".py, after the Battle of the Brandywine River, and "nile".py, after the Battle of the Nile. Within the gamefiles/ directory, a file called gamefile_template.py is included as an example so that the user can make his own gamefile. 

Kriegsspiel is highly documented, with most of the documentation found in the directory documentation/. Rules for the game itself are contained within Eschaton Fifth Edition. The license, changelog, and release notes can also be found within documentation/. 