# kriegsspiel

This is a Python script for use by the Umpire in managing a game of Kriegsspiel.
It is as yet incomplete.

For more information on the game rules themselves, see the .docx document.

Effectively, the script works by importing a gamefile, which creates the particular scenario.

A game loop cycles, asking for commands from the user. Based on this input, kriegsspiel.py calls various functions based on the game commands. These functions will then do math on the variables imported by the gamefile, and adjusts their attribute lists as such.

Structure:
README.md - this file, the readme itself
CHANGELOG - contains a history of commit versions and their numbers
LICENSE - GNU General Public License version 3
Kriegspiel Third Edition.docx - the whitepaper from which this game was derived
kriegsspiel.py - core file, contains most of the principal functions and the game loop
gamefiles/ - contains various scenarios that can be played
gamefiles/scenariotemplate.py - template for creating a new gamefile
manpages/ - contains textfile explanations of various commands