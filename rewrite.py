import random
import os
from brandywine import *

round = 1
usedUnits = []
immobileUnits = []
hiddenUnits = []
alreadyDropped = []
commandNumber = 1
secrets = ""
oneWordCommands = {"score":"score", "turn":"turn", "quit":"quitGame", "help":"helpText", "attack":"attack", "details":"details"}

def move(unit, unitType, team):
    pass

def heading(unit, unitType, team):
    pass

def hide(unit, unitType, team):
    pass

def reveal(unit, unitType, team):
    pass

def spy(unit, unitType, team):
    pass

def fire(unit, unitType, team):
    pass

def build(unit, unitType, team):
    pass

def torpedo(unit, unitType, team):
    pass

def sortie(unit, unitType, team):
    pass

def depthcharge(unit, unitType, team):
    pass

def man(command, arg2, arg3):
    pass

def attack():
    pass

def health(unit, unitType, team):
    pass

def kill(unit, unitType, team):
    pass

def freeze(unit, unitType, team):
    pass

def score():
    pass

def details():
    pass

def turn():
    global round
    usedUnits.clear()
    immobileUnits.clear()
    alreadyDropped.clear()
    round = round + 1

def info(unit, unitType, team):
    pass

def quitGame():
    score()
    quit()

def helpText():
    global validCommands
    global allUnitTypes
    print("turn, quit, man, help, details, score")
    print(*validCommands, sep = ", ")
    print(*allUnitTypes, sep = ", ")
    print("To learn more about any command, type 'man [command]'.")

def throwError(function):
    if function == "arguments": errorMessage = "Too many arguments for command."
    elif function == "bad": errorMessage = "Bad command."
    print(errorMessage)

def shell(team):
    global commandNumber
    prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + team + "]% "
    rawCommand = input(prompt)
    if len(rawCommand.split()) > 2: 
        throwError("arguments")
        return
    elif len(rawCommand.split()) == 2:
        command, unit = rawCommand.split()
        unitType = unitTable.get(unit)
        if command in validCommands: globals()[command](unit, unitType, team)
        else: 
            throwError("bad")
            return
    else: 
        try: globals()[oneWordCommands.get(rawCommand)]()
        except: 
            throwError("bad")
            return
    commandNumber = commandNumber + 1

while True:
    while (round % 2) != 0: shell(firstTeam)
    while (round % 2) == 0: shell(secondTeam)