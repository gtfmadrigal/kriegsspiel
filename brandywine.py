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
validCommands = ["move", "attack", "fire", "build", "hide", "search", "spy", "convert", "info", "manual"]

# Unique to game scenario
rebelDamage = 0
britishDamage = 0
rebelHealth = 276
britishHealth = 334 

# Functions

# def move(unit)
# def attack(unit)
# def fire(unit)
# def build(unit)
# def hide(unit)
# def search(unit)
# def spy(unit)
# def convert(unit)
# def info(unit)
# def manual(unit)

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
        print("Meta commands: help, info, turn, quit, details, manual")
        print("Unit commands: move, attack, fire, build, hide, search, spy, convert")
    elif command == "details": print(secrets)
    elif command == "score": score()
    elif command in validCommands:
        unit = input("[unit]% ")
        getCommand(command, unit)
    else: print("Unknown command.")
    commandNumber = commandNumber + 1