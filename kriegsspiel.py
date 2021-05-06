import random
from brandywine import *

# Global variables and lists
warPhase = True
round = 1
usedUnits = []
immovableUnits = []
deadUnits = []
commandNumber = 1
secrets = ""
hiddenUnits = []

# Unique to game scenario
firstDamage = 0
secondDamage = 0
firstHealth = 276
secondHealth = 334 

# Functions
def move(unit, unitType):
    global immovableUnits
    global usedUnits
    if unit in immovableUnits:
        print("Immovable.")
        return
    if not unitType in moveAndFire:
        usedUnits.append(unit)
    immovableUnits.append(unit)

# def attack(unit, unitType):
# def fire(unit)
# def build(unit)
# def hide(unit)
# def search(unit)
# def spy(unit)

# Universal functions
def getCommand(command, unit, unitType):
    if unit in deadUnits:
        print("Dead.")
        return
    elif unit in usedUnits:
        print("Used.")
    if command == "move": move(unit, unitType)
    elif command == "attack": attack(unit, unitType)
    # elif command == "fire": fire(unit)
    # elif command == "build": build(unit)
    # elif command == "hide": hide(unit)
    # elif command == "search": search(unit)
    # elif command == "spy": spy(unit, unitType)
    elif command == "info": 
        info(unitType)
        if unit in deadUnits: print("Dead.")
        if unit in immovableUnits: print("Immovable this turn.")
        if unit in usedUnits: print("Unusable this turn.")
    else: "Unknown command."

def manual(argument):
    global firstDamage
    global secondDamage
    global deadUnits
    global immovableUnits
    if argument == "help": print("Arguments for manual() function: health, kill, freeze.")
    elif argument == "health":
        score()
        teamToChange = input(manualHelpPrompt)
        newValue = int(input("New health value: "))
        if teamToChange == "b": firstDamage = secondHealth - newValue
        else: secondDamage = firstHealth - newValue
    elif argument == "kill":
        currentValue = int(input("Current value of unit: "))
        namedUnit = input("Name of unit: ")
        deadUnits.append(namedUnit)
        owner = input(ownerPrompt)
        if owner == "b": firstDamage = firstDamage + currentValue
        else: secondDamage = secondDamage + currentValue
    elif argument == "freeze":
        namedUnit = input("Name of unit: ")
        owner = input(ownerPrompt)
        immovableUnits.append(namedUnit)
    else:
        print("Bad argument for manual function.")
        return

def score():
    print(firstTeam, "damage dealt:", firstDamage)
    print(secondTeam, "damage dealt:", secondDamage)
    firstPercent = (firstHealth - secondDamage) / firstHealth * 100
    secondPercent = (secondHealth - firstDamage) / secondHealth * 100
    print(firstTeam, "percent remaining:", firstPercent)
    print(secondTeam, "percent remaining:", secondPercent)

# Game loop
while warPhase == True:
    prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "]% "
    command = input(prompt)
    if command == "turn":
        usedUnits.clear()
        immovableUnits.clear()
        round = round + 1
    elif command == "quit": 
        score()
        warPhase = False
    elif command == "help":
        print("turn, quit, help, details, score, new")
        print(*validCommands, sep = ", ") 
    elif command == "details": print(secrets)
    elif command == "score": score()
    elif command == "manual":
        subPrompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + command + "]% "
        argument = input(subPrompt)
        manual(argument)
    elif command == "new": newGame()
    elif command in validCommands:
        subPrompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + command + "]% "
        unit, unitType = input(subPrompt).split()
        getCommand(command, unit, unitType)
    else: print("Unknown command.")
    commandNumber = commandNumber + 1