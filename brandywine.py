import random

# Global variables and lists
warPhase = True
round = 1
usedUnits = []
immovableUnits = []
deadUnits = []
commandNumber = 1
secrets = ""
hiddenUnits = []
validCommands = ["attack", "fire", "build", "hide", "search", "spy", "convert", "info", "manual"]

# Unique to game scenario
rebelDamage = 0
britishDamage = 0
rebelHealth = 276
britishHealth = 334 

# Functions

# Game-specific functions
# def attack(unit)
# def fire(unit)
# def build(unit)
# def hide(unit)
# def search(unit)
# def spy(unit)
# def convert(unit)
# def info(unit)

# Universal functions
# def getCommand(unit):

def manual(argument):
    if argument == "help": print("Arguments for manual() function: health, kill, freeze.")
    elif argument == "health":
        score()
        newValue = int(input("New health value: "))
        teamToChange = input("Alter Rebel or British health? [R/b]: ")
        if teamToChange == "b": 
            global rebelDamage
            rebelDamage = britishHealth - newValue
        else:
            global britishDamage
            britishDamage = rebelHealth - newValue
    # elif argument == "kill"
    # elif argument == "freeze"
    else:
        print("Bad argument for manual function.")
        return

def score():
    print("Rebel damage dealt:", rebelDamage)
    print("British damage dealt:", britishDamage)
    rebelPercent = (rebelHealth - britishDamage) / rebelHealth * 100
    britishPercent = (britishHealth - rebelDamage) / britishHealth * 100
    print("Rebel percent remaining:", rebelPercent)
    print("British percent remaining:", britishPercent)

# Game loop
while warPhase == True:
    print("Round:", round)
    print("Command:", commandNumber)
    command = input("% ")
    if command == "turn":
        usedUnits.clear()
        immovableUnits.clear()
        round = round + 1
    elif command == "quit": 
        score()
        warPhase = False
    elif command == "help":
        print("Meta commands: new, help, info, turn, quit, details, manual")
        print("Unit commands: attack, fire, build, hide, search, spy, convert")
    elif command == "details": print(secrets)
    elif command == "score": score()
    elif command == "new": newGame()
    elif command == "manual":
        argument = input("[manual]% ")
        manual(argument)
    elif command in validCommands:
        unit = input("[unit]% ")
        getCommand(command, unit)
    else: print("Unknown command.")
    commandNumber = commandNumber + 1