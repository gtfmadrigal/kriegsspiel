# Imports
import random
from setup.py import *

# Universal variables
warPhase = True
round = 1
usedUnits = []
deadUnits = []
immovableUnits = [highCommand]
commandNumber = 1
secrets = ""
hiddenUnits = []

# Functions
def getCommand(command, unit): # Primary function
    if globals()[unit] in deadUnits:
        print(globals()[unit], " is dead.")
        return
    if command == "move": move(unit)
    elif command == "attack": attack(unit)
    elif command == "fire": fire(unit)
    elif command == "build": build(unit)
    elif command == "hide": hide(unit)
    elif command == "search": search(unit)
    elif command == "convert": convert(unit)
    elif command == "spy": spy()
    elif command == "endTurn": turnPortion = turnPortion + 1
    elif command == "endGame": warPhase = False
    elif command == "help": help()
    elif command == "info": info(unit)
    elif command == "details": details()
    elif command == "manual": manual(unit)
    else: 
        print("Unknown command.")
        return
    commandNumber = commandNumber + 1

def move(unit):
    if globals()[unit] in immovableUnits:
        print(globals()[unit], " is immovable.")
        return
    print(globals()[unit], " is moved.")
    immovableUnits.append(globals()[unit])
    if not globals()[unit] in moveAndFire:
        usedUnits.append(globals()[unit])

# def attack(unit):
# def fire(unit):
def build(unit):
    if not globals()[unit] in build:
        print(globals()[unit], " cannot build.")
        return
    elif globals()[unit] in usedUnits:
        print(globals()[unit], " cannot build.")
        return
    elif globals()[unit] in d4_build:
        fortificationStrength = random.randrange(1,4)
    else:
        fortificationStrength = random.randrande(1,8) 
    print("Fortification of strength ", fortificationStrength, " built.")
    usedUnits.append(globals()[unit])
    immovableUnits.append(globals()[unit])

def hide(unit):
    if not globals()[unit] in hide:
        print(globals()[unit], " cannot hide.")
        return
    elif globals()[unit] in usedUnits:
        print(globals()[unit], " cannot hide.")
        return
    elif globals()[unit] in hiddenUnits:
        print(globals()[unit], " is already hidden.")
        return
    secretLocation = input("Location to hide: ")
    secrets = secrets + " " + secretLocation
    print(globals()[unit], " hidden.")
    hiddenUnits.append(globals()[unit])
    usedUnits.append(globals()[unit])
    immovableUnits.append(globals()[unit])

def search(unit):
    if not globals()[unit] in search:
        print(globals()[unit], " cannot search.")
        return
    elif globals()[unit] in usedUnits:
        print(globals()[unit], " cannot search.")
        return
    searchEfficacy = random.randrange(1,6)
    if searchEfficacy == 6:
        print("Perfect information.")
    elif searchEfficacy == 1:
        print("Bad information.")
    else:
        print("No information.")
    usedUnits.append(globals()[unit])
    immovableUnits.append(globals()[unit])

def convert(unit):
    if not globals()[unit] in artillery:
        print(globals()[unit], " cannot be converted or is already infantry.")
        return
    elif globals()[unit] in usedUnits:
        print(globals()[unit], " cannot be converted or is already infantry.")
        return
    elif globals()[unit] in grenadiers: grenadiers.remove(globals()[unit])
    elif globals()[unit] in bombadiers: bombadiers.remove(globals()[unit])
    elif globals()[unit] in hussars: hussars.remove(globals()[unit])
    elif globals()[unit] in dragoons: dragoons.remove(globals()[unit])
    infantry.append(globals()[unit])
    usedUnits.append(globals()[unit])
    immovableUnits.append(globals()[unit])

def spy(unit):
    if not globals()[unit] in spy:
        print(globals()[unit], " cannot spy for information.")
        return
    elif globals()[unit] in usedUnits:
        print(globals()[unit], " cannot spy for information.")
        return
    spyEfficacy = random.randrange(1,6)
    usedUnits.append(globals()[unit])
    immovableUnits.append(globals()[unit])
    if spyEfficacy == 1:
        print("Give bad information:")
        print(secrets)
    elif spyEfficacy == 6:
        print("Give perfect information:")
        print(secrets)
    else:
        print("Give no information.")
    
def help():
    print("Informational commands: help, info, endGame, details, manual")
    print("Game commands: move, attack, fire, build, hide, search, convert, spy, endTurn")

def info(unit):
    print("Attributes of unit " unit)
    if globals()[unit] in usedUnits: print("Unusable this turn.")
    if globals()[unit] in deadUnits: print("Dead.")
    if globals()[unit] in immovableUnits: print("Immovable this turn.")
    if globals()[unit] in hiddenUnits: print("Hidden.")
    if globals()[unit] in infantry: print("Infantry: D4 small arms, D4 build, can search, hide, and move and fire.")
    if globals()[unit] in sappers: print("Sapper: D4 small arms, D8 build, can search, hide, and move and fire.")
    if globals()[unit] in fusiliers: print("Fusilier: D4 small arms, can search, hide, and move and fire.")
    if globals()[unit] in grenadiers: print("Grenadier: D4 small arms, D8 artillery, can hide.")
    if globals()[unit] in bombadiers: print("Bombadier: D4 small arms, D10 artillery.")
    if globals()[unit] in hussars: print("Hussar: D12 small arms and artillery, can move and fire.")
    if globals()[unit] in dragoons: print("Dragoon: D20 small arms and artillery, can move and fire.")
    if globals()[unit] in special: print("Special: D20 small arms, can hide, and move and fire.")
    if globals()[unit] in spy: print("Spy: D4 small arms, always hidden, no special abilities.")
    if globals()[unit] in highCommand: print("High command: D20 small arms, immovable.")

def details():
    print(secrets)
    print("French percentage: ", frenchPercentage)
    print("British percentage: ", britishPercentage)

def manual(unit):
    print("Manual adjustment commands: newValue, changeList, clearList, exit")
    adjustment = input("Adjustment command: ")
    if adjustment == "newValue":
        newValue = input("New health value for ", unit, ", currently ", globals()[unit], ": ")
        globals()[unit] = newValue
        if newValue == 0:
            deadUnits.append(globals()[unit])
    elif adjustment == "changeList":
        print("Attribute lists: usedUnits, deadUnits, immovableUnits, hiddenUnits")
        print("Categorical lists: infantry, sappers, fusiliers, grenadiers, bombadiers, hussars, dragoons, special, spy, highCommand")
        newList = input("List to add/remove", unit, " from: ")
        if globals()[unit] in globals()[newList]:
            globals()[newList].remove(globals()[unit])
        else:
            globals()[newList].append(globals()[unit])
    elif adjustment == "clearList":
        print("Attribute lists: usedUnits, deadUnits, immovableUnits, hiddenUnits")
        listToClear = input("List to clear: ")
        globals()[listToClear].clear()
    elif adjustment == "exit":
        return
    else:
        print("Bad command. Try again.")
        return
        
# Game loop
while warPhase == True:
    turnPortion = 1
    print("Round: ",round)
    usedUnits.clear()
    immovableUnits.clear()
    immovableUnits.append(highCommand)
    while turnPortion == 1:
        command, unit = input("[British] [", commandNumber, "]$ ").split()
        getCommand(command, unit)
    usedUnits.clear()
    immovableUnits.clear()
    immovableUnits.append(highCommand)
    while turnPortion == 2:
        command, unit = input("[French] [", commandNumber, "]$ ").split()
        getCommand(command, unit)
    roundNumber = roundNumber + 1