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
    if not unitType in moveAndFire: usedUnits.append(unit)
    immovableUnits.append(unit)

def attack(unit, unitType):
    global immovableUnits
    global usedUnits
    global deadUnits
    global hiddenUnits
    global firstDamage
    global secondDamage
    if unit in hiddenUnits:
        print("Unit revealed.")
        reveal(unit, unitType)
        return
    if unitType in attack4: maximum = 4
    elif unitType in attack12: maximum = 12
    elif unitType in attack20: maximum = 20
    damageDealt = random.randrange(1,maximum)
    owner = input(ownerPrompt)
    if owner == "a": 
        firstDamage = firstDamage + damageDealt
        print(firstTeam, "deal", damageDealt, "damage.")
    else: 
        secondDamage = secondDamage + damageDealt
        print(secondTeam, "deal", damageDealt, "damage.")
    print("Manually enter any dead units using the manual(kill) command.")
    usedUnits.append(unit)
    immovableUnits.append(unit)


# def fire(unit, unitType):

def build(unit, unitType):
    global immovableUnits
    global usedUnits
    if not unitType in buildable:
        print("Cannot build.")
        return
    if unitType in build4: print("Fortification of strength", random.randrange(1,4), "built.")
    elif unitType in build8: print("Fortification of strength", random.randrange(1,8), "built.")
    immovableUnits.append(unit)
    usedUnits.append(unit)

def hide(unit, unitType):
    global hiddenUnits
    global secrets
    if not unitType in hideable:
        print("Cannot hide.")
        return
    if unit in hiddenUnits:
        print("Already hidden.")
        return
    hiddenUnits.append(unit)
    newSecret = input("Describe information about this command: ")
    secrets = secrets + ", " + newSecret

def reveal(unit, unitType):
    global hiddenUnits
    if not unit in hiddenUnits:
        print("Not hidden.")
        return
    hiddenUnits.remove(unit)

def search(unit, unitType):
    global usedUnits
    if not unitType in searchable:
        print("Cannot search.")
        return
    searchEffectiveness = random.randrange(1,6)
    if searchEffectiveness == 6:
        print("Good formation.")
        print(secrets)
    elif searchEffectiveness ==1:
        print("Bad information.")
        print(secrets)
    else: print("No information.")
    usedUnits.append(unit)

def spy(unit, unitType):
    global usedUnits
    if not unitType in deadUnits: maximum = 8
    else: maximum = 6
    spyEffectiveness = random.randrange(1,maximum)
    if spyEffectiveness >= 6: 
        print("Good information.")
        print(secrets)
    elif spyEffectiveness == 1: 
        print("Bad information.")
        print(secrets)
    else: print("No information.")
    usedUnits.append(unit)

# def torpedo(unit, unitType):
# def sortie(unit, unitType):
# def missile(unit, unitType):
# def dropcharge(unit, unitType):

# Universal functions
def getCommand(command, unit, unitType):
    if unit in deadUnits:
        print("Dead.")
        return
    elif unit in usedUnits:
        print("Used.")
        return
    if command == "move": move(unit, unitType)
    elif command == "attack": attack(unit, unitType)
    # elif command == "fire": fire(unit, unitType)
    elif command == "build": build(unit, unitType)
    elif command == "hide": hide(unit, unitType)
    elif command == "reveal": reveal(unit, unitType)
    elif command == "search": search(unit, unitType)
    elif command == "spy": spy(unit, unitType)
    # elif command == "torpedo": torpedo(unit, unitType)
    # elif command == "sortie": sortie(unit, unitType)
    # elif command == "missile": missile(unit, unitType)
    # elif command == "dropcharge": missile(unit, unitType)
    elif command == "info": 
        info(unitType)
        if unit in deadUnits: print("Dead.")
        if unit in immovableUnits: print("Immovable this turn.")
        if unit in usedUnits: print("Unusable this turn.")
        if unit in hiddenUnits: print("Hidden.")
    else: print("Unknown command.")

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