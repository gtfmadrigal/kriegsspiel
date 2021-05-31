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

def attack(team, arg2, arg3):
    pass

def health(unit, unitType, team):
    pass

def kill(unit, unitType, team):
    pass

def freeze(unit, unitType, team):
    pass

def score(unit, unitType, team):
    pass

def details(unit, unitType, team):
    pass

def turn(unit, unitType, team):
    global round
    round += 1
    pass

def info(unit, unitType, team):
    pass

def quitGame(unit, unitType, team):
    pass

def helpText(unit, unitType, team):
    pass

def throwError(function):
    if function == "arguments": return
    elif function == "bad": return
    pass

def shell(team, prompt):
    global commandNumber
    rawCommand = input(prompt)
    if len(rawCommand.split()) > 2: 
        throwError("arguments")
        return
    elif len(rawCommand.split()) == 2:
        command, unit = rawCommand.split()
        unitType = unitTable.get(unit)
        if command in validCommands: globals()[command](unit, unitType, team)
    else:
        oneWordCommands = {"score":"score", "turn":"turn", "quit":"quitGame", "help":"helpText", "attack":"attack", "details":"details"}
        actualFunction = oneWordCommands.get(rawCommand, "None")
        if actualFunction == "None": 
            throwError("bad")
            return
        globals()[actualFunction](0,0,0)
    commandNumber += 1


while True:
    while (round % 2) != 0:
        prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + str(firstTeam) + "]% "
        team = firstTeam
        shell(team, prompt)
    while (round % 2) != 0:
        prompt = "[Rd." + str(round) + "][" + str(commandNumber) = "][" + str(secondTeam) + "]% "
        team = secondTeam
        shell(team, prompt)