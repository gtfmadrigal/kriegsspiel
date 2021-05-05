# Imports
import random
from brandywine import * # gamefile import

# Functional imports
from attack import *
from build import *
from convert import *
from fire import *
from hide import *
from move import *
from search import *
from spy import *

# Universal variables
warPhase = True
round = 1
usedUnits = []
deadUnits = []
immovableUnits = [highCommand]
commandNumber = 1
secrets = ""
hiddenUnits = []
validCommands = ["move", "attack", "fire", "build", "hide", "search", "spy", "convert", "info", "manual"]

# Functions
def getCommand(command, unit): # Primary function
    if globals()[unit] in deadUnits:
        print(unit, "is dead.")
        return
    if command == "move": move(unit)
    elif command == "attack": attack(unit)
    elif command == "fire": fire(unit)
    elif command == "build": build(unit)
    elif command == "hide": hide(unit)
    elif command == "search": search(unit)
    elif command == "spy": spy(unit)
    elif command == "convert": convert(unit)
    elif command == "info": info(unit)
    elif command == "manual": manual(unit)
        
# Game loop
while warPhase == True:
    print("Round:", round)
    print("Command: ", commandNumber)
    command = input("% ")
    if command == "endTurn":
        usedUnits.clear()
        immovableUnits.clear()
        immovableUnits.append(britishHighCommand)
        immovableUnits.append(frenchHighCommand)
        round = round + 1
    elif command == "endGame": warPhase = False
    elif command == "help":
        print("Informational commands: help, info, endGame, details, manual")
        print("Game commands: move, attack, fire, build, hide, search, convert, spy, endTurn")
    elif command == "details": print(secrets)
    elif command in validCommands:
        unit = input("[unit]% ")
        getCommand(command, unit)
    else:
        print("Unknown command.")
    commandNumber = commandNumber + 1

gameEnd()