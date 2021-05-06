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
# def move(unit)
# def attack(unit)
# def fire(unit)
# def build(unit)
# def hide(unit)
# def search(unit)
# def spy(unit)

# Universal functions
def getCommand(command, unit, unitType):
    if command == "move": move(unit)
    # elif command == "attack": attack(unit)
    # elif command == "fire": fire(unit)
    # elif command == "build": build(unit)
    # elif command == "hide": hide(unit)
    # elif command == "search": search(unit)
    # elif command == "spy": spy(unit, unitType)
    elif command == "info": 
        info(unitType)
        if unit in deadUnits: print("Dead.")
    else: "Unknown command."

def manual(unit):
    global firstDamage
    global secondDamage
    global deadUnits
    global immovableUnits
    if unit == "help": print("Arguments for manual() function: health, kill, freeze.")
    elif unit == "health":
        score()
        teamToChange = input(manualHelpPrompt)
        newValue = int(input("New health value: "))
        if teamToChange == "b": firstDamage = secondHealth - newValue
        else: secondDamage = firstHealth - newValue
    elif unit == "kill":
        currentValue = int(input("Current value of unit: "))
        namedUnit = input("Name of unit: ")
        deadUnits.append(namedUnit)
        owner = input(ownerPrompt)
        if owner == "b": firstDamage = firstDamage + currentValue
        else: secondDamage = secondDamage + currentValue
    elif unit == "freeze":
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
        unit = input(subPrompt)
        manual(unit)
    elif command == "new": newGame()
    elif command in validCommands:
        subPrompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + command + "]% "
        unit, unitType = input(subPrompt).split()
        getCommand(command, unit, unitType)
    else: print("Unknown command.")
    commandNumber = commandNumber + 1