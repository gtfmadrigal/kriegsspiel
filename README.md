# kriegsspiel

This is a Python script for use by the Umpire in managing a game of Kriegsspiel.
It is as yet incomplete.

For more information on the game rules themselves, see the .docx document.

Effectively, the script works by importing a gamefile, which creates the particular scenario.

A game loop cycles, asking for commands from the user. Based on this input, kriegsspiel.py calls various functions based on the game commands. These functions will then do math on the variables imported by the gamefile, and adjusts their attribute lists as such.
