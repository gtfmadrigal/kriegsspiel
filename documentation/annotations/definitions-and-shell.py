# This is an annotated version of kriegsspiel.py. I removed all of the comments from the original and converted them here, since the comments were becoming long and burdensome.
# This version is NON-RUNNABLE. If you are opening this with Visual Studio or some other Python IDE, running it will not work. It is meant for research and documentation purposes only. Primarily, the reason that this is the case is because the functions are juggled around in order to make documentation easier. 
# Essentially, this program is divided into four sections: definitions and imports, the game loop and shell, meta-functions, and callable functions.

# Part I: Definitions and Imports

# I-a. Imports
import random # random.randrange() sed only by the evaluate() meta function to simulate rolling dice with a computer.
import os # os.name() used only by the man() callable function. See man() for more.
from nile import * # Most important import statement. Replace "nile" with the name of whatever gamefile you want to use. When doing this, move the gamefile from the gamefiles/ directory to the main one, alongside kriegsspiel.py. Notice that the ordinary "import module" statement is not used here like it is for the random and os modules. "from module import *" is generally not recommened, since it is a security flaw, but in this case, we are only importing a single Python file, full of definitions, created by the user. However, since this is a security hole, I recommend that anyone using this program check a gamefile downloaded from another user.

# I-b. Definitions
round = 1 # Sets the round equal to 1 initially, so that the shell has a number to work with before turn() is called.
usedUnits = [] # All lists defined in this list are to contain strings, containing the names of various units. This list contains units that have already been used in the current turn. It is cleared every turn.
immobileUnits = [] # Units that have already moved or taken an action which prevents it from moving are contained in this list, which is again cleared at the end of every turn.
hiddenUnits = [] # Units that are hidden are stored here. hide() appends units to this list, reveal() removes them from it.
alreadyDropped = [] # depthcharge() cannot only be called once per unit, but a unit that drops depth charges can also perform other commands, so another list needs to be added exclusively for the depthcharge() function to use. Cleared every turn.
defendingUnits = [] # In fire() and attack(), a list of units defending needs to be looped through to ensure clean attribution of damages.
doubleImmobileUnits = [] # depthcharge() can immobilize a submarine during the next turn. As such, another list needs to exist to ensure that units are re-added to the immobileUnits list.
deadUnits = [] # While not strictly required, the deadUnits list is included for ease of searching
commandNumber = 1 # Sets the commandNumber to 1 intially, so that the shell has a number to work with at the beginning of the game
secrets = "" # Empty string originally, added to when hide() is called, so that the umpire can keep track of the secret locations.
oneWordCommands = {"score":"score", "turn":"turn", "quit":"quitGame", "help":"helpText", "attack":"attack", "details":"details"} # One word commands are dealt with specially by the shell, and some in-game commands are reserved Python keywords (namely, "quit" and "help"). Since the functions "quit" and "attack" cannot exist, they are mapped to quitGame() and helpText(). Therefore, the shell will recognize a one-word command and instead of calling the command itself, will call the value that the command-as-key is mapped to in this dictionary.

# Part II: Game Loop and Shell

# II-a. Shell
def shell(team, targetTeam, targetTeamTable, teamTable): # All arguments are received from the main game loop.
    global commandNumber # The command number has to be made global in order to be updated by the function 
    prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + team + "]% " # The prompt contains the round, command number and the team when used by the shell. Later on, when another command requires user input, the command will also be included in the prompt.
    rawCommand = input(prompt) # The unparsed command is called rawCommand.
    if len(rawCommand.split()) > 2: # If the length of the unparsed command is greater than 2, an error is thrown, because no command needs more than a single argument.
        throwError("arguments")
        return
    elif len(rawCommand.split()) == 2: # If the command is exactly two words long, it must be a regular game function.
        command, unit = rawCommand.split() # The rawCommand is spliced into the command and the unit.
        unitType = unitTable.get(unit) # The unitType is retrieved from the unitTable dictionary. If the unit does not exist, unitType will have a value of None, but this is not a problem until a command is actually called.
        if command in validCommands: globals()[command](unit, unitType, team, targetTeam, targetTeamTable, teamTable) # If the command is valid (i.e. if it is in the validCommands list), a function with the same name as the command variable is called, and the various relevant arguments are passed. 
        else: # If a command is not valid, an error is thrown and the function is returned to the game loop.
            throwError("bad")
            return
    else: # If the command is one word long, a one-word-command is called
        if rawCommand == "attack": attack(team, targetTeam, targetTeamTable, teamTable) # If the raw command is attack (which is a regular game function), various arguments are passed
        else: # Otherwise, the command must be a meta-function
            try: globals()[oneWordCommands.get(rawCommand)]() # The calling of a one-word function is held within a try-except statement, becuase if the function does not exist, an error would otherwise by thrown and the whole program would crash. Hence, the globals() function is only tried.
            except: # If the function is bad, and an error would ordinarily be called, an error is thrown and the program returns to the game loop.
                throwError("bad")
                return
    commandNumber = commandNumber + 1 # The command number is incremented before returning the game loop.

# II-b. Main game loop
while True: # Loop runs permanently, until the quitGame() function is called.
    while (round % 2) != 0: shell(firstTeam, secondTeam, secondTeamTable, firstTeamTable) # If the round is odd, the team is the first team.
    while (round % 2) == 0: shell(secondTeam, firstTeam, firstTeamTable, secondTeamTable) # If the round is even, the team is the second one.