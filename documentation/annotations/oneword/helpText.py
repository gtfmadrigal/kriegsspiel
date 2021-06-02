# helpText() is a callable function using the one-word command "help". It is not called by any other function.

def helpText(): # No arguments are taken, since the function is game-wide
    print("turn, quit, help, details, attack, score") # This is a list of one-word commands that are not required to be included in the validCommands list from the gamefile.
    print(*validCommands, sep = ", ") # The valid commands are listed from the gamefile
    print(*allUnitTypes, sep = ", ") # A list of all unit types are listed from the gamefile
    print("To learn more about any command, type 'man [command]'.")