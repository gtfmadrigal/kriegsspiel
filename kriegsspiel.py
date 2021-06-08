import random
import os
from normandy import *

round = 1
usedUnits = []
immobileUnits = []
hiddenUnits = []
alreadyDropped = []
defendingUnits = []
doubleImmobileUnits = []
deadUnits = []
commandNumber = 1
secrets = ""
errorMessages = {"arguments":"Too many arguments for command. Type 'man' [command] for information.", "os":"Unknown operating system.", "bad":"Bad command. Type 'help' for assistance.", "team":"That unit does not belong to you.", "available":"That unit is currently unavailable.", "function":"That function is unavailable to this unit.", "heading":"Unit cannot exceed its maximum heading change.", "dead":"Unit is dead.", "type":"No such unit type.", "unit":"No such unit.", "hidden":"Unit is already hidden.", "required":"Heading changes are not required for this unit."}
agnosticCommands = ["move", "hide", "reveal", "spy", "fire", "convert"]
navyCommands = ["heading", "torpedo", "sortie", "depthcharge", "load", "disembark"]
armyCommands = ["build"]
airCommands = ["takeoff", "land", "pulse", "airlift", "survey", "bomb"]
umpireCommands = ["health", "kill", "freeze", "disable"]
airPhase = True

# Meta-functions
def meta_update():
    global firstHealth
    global secondHealth
    global firstTeamTable
    global secondTeamTable
    firstHealth = sum(firstTeamTable.values())
    secondHealth = sum(secondTeamTable.values())

def meta_changeList(unit, list, command):
    global usedUnits
    global immobileUnits
    global hiddenUnits
    if command == "append": list.append(unit)
    elif command == "clear": list.clear()
    elif command == "remove": list.remove(unit)

def meta_evaluate(unit, unitType, table):
    if unit in immobileUnits or unit in usedUnits:
        print(errorMessages.get("available"))
        return
    if unit in deadUnits:
        print(errorMessages.get("dead"))
        return
    if table.get(unitType) == None: return
    return random.randrange(1, table.get(unitType) + 1)

# One-word command functions
def score():
    pass

def turn():
    pass

def details():
    pass

def quitGame():
    pass

def helpText():
    pass

def attack():
    pass

# Umpire functions

def health():
    pass

def kill():
    pass

def freeze():
    pass

def disable():
    pass

def merge():
    pass

def split():
    pass

# Theater-agnostic functions
def move(unit, unitType):
    if unit in immobileUnits:
        print(errorMessages.get("function"))
        return
    if unitType in headingTable: print(errorMessages.get("heading"))
    if not unitType in moveFireTable: meta_changeList(unit, usedUnits, "append")
    meta_changeList(unit, immobileUnits, "append")

def hide(unit, unitType, team):
    global secrets
    if not unitType in hideTable:
        print(errorMessages.get("function"))
        return
    if unit in hiddenUnits:
        print(errorMessages.get("hidden"))
        return
    prompt = str(round) + " ~ " + str(commandNumber) + " " + str(team) + " > hide % "
    location = input(prompt)
    newSecret = unit + " " + location
    secrets = secrets + ", " + newSecret
    meta_changeList(unit, hiddenUnits, "append")

def reveal(unit, unitType):
    global secrets
    if not unit in hiddenUnits or not unitType in hideTable:
        print(errorMessages.get("function"))
        return
    meta_changeList(unit, hiddenUnits, "remove")
    append = unit + "is no longer hidden."
    secrets = secrets + append

def spy(unit, unitType):
    effectiveness = meta_evaluate(unit, unitType, spyTable)
    if effectiveness == 6: print("Good information.")
    elif effectiveness == 1: print("Bad information.")
    elif effectiveness == None: return
    else: print("No information.")
    details()
    meta_changeList(unit, usedUnits, "append")

def fire(unit, unitType, team, targetTeamTable):
    global firstTeamTable
    global secondTeamTable
    defensePhase = True
    willQuit = False
    if not unitType in fireTable:
        print(errorMessages.get("function"))
        return
    while defensePhase == True:
        prompt = str(round) + " ~ " + str(commandNumber) + " " + str(team) + " > fire % "
        command = input(prompt)
        if command == "help": print("Enter a named unit, 'save' to save changes to gamestate, or 'quit' to exit without saving.")
        elif command == "quit":
            defensePhase = False
            willQuit = True
        elif command == "save": defensePhase = False
        elif command in unitTable:
            try: meta_changeList(command, defendingUnits, "append")
            except: pass
        else: print(errorMessages.get("bad"))
    if willQuit == True: return
    damage = meta_evaluate(unit, unitType, fireTable)
    print("Damage:", damage)
    perUnitDamage = damage / len(defendingUnits)
    print("Damage per unit:", perUnitDamage)
    for x in defendingUnits:
        oldHealth = targetTeamTable.get(x)
        if oldHealth - perUnitDamage < 0: 
            newHealth = 0
            print(x, "killed.")
        else: 
            newHealth = oldHealth - perUnitDamage
            print(x, "new health:", newHealth)
        targetTeamTable[x] = newHealth
    meta_changeList(True, defendingUnits, "clear")
    score()
    turn()

def convert():
    pass

# Naval functions
def heading(unit, unitType):
    if meta_evaluate(unit, unitType, headingTable) == 1:
        meta_changeList(unit, immobileUnits, "append")
        if not unitType in moveFireTable: meta_changeList(unit, usedUnits, "append")
    else:
        print(errorMessages.get("required"))
        return

def torpedo():
    pass

def sortie():
    pass

def depthcharge():
    pass

def load():
    pass

def disembark():
    pass

# Army functions
def build():
    pass

# Air functions
def takeoff():
    pass

def land():
    pass

def pulse():
    pass

def airlift():
    pass

def survey():
    pass

def bomb():
    pass

# Shell
def info():
    pass

def agnosticShell(command, unit, team, targetTeam, teamTable, targetTeamTable):
    if not unit in teamTable:
        print(errorMessages.get("team"))
        return
    unitType = unitTable.get(unit)
    if command == "move": move(unit, unitType)
    elif command == "hide": hide(unit, unitType, team)
    elif command == "reveal": reveal(unit, unitType)
    elif command == "spy": spy(unit, unitType)
    elif command == "fire": fire(unit, unitType, team, targetTeamTable)
    elif command == "convert": pass

def navyShell(command, unit, team, targetTeam, teamTable, targetTeamTable):
    if not unit in teamTable:
        print(errorMessages.get("team"))
        return
    unitType = unitTable.get(unit)
    if command == "heading": heading(unit, unitType)
    elif command == "torpedo": pass
    elif command == "sortie": pass
    elif command == "depthcharge": pass
    elif command == "load": pass
    elif command == "disembark": pass

def armyShell(command, unit, team, targetTeam, teamTable, targetTeamTable):
    if command == "build": pass

def umpireShell(command, unit, team, targetTeam, teamTable, targetTeamTable):
    if command == "health": health()
    elif command == "kill": kill()
    elif command == "freeze": freeze()
    elif command == "disable": disable()
    elif command == "merge": merge()
    elif command == "split": split()

def airShell(team, targetTeam, teamTable, targetTeamTable):
    global commandNumber
    global airPhase
    prompt = str(round) + " ~ " + str(commandNumber) + " " + str(team) + "-air" + " % "
    rawCommand = input(prompt)
    if len(rawCommand.split()) == 2:
        command, unit = rawCommand.split()
        if command == "takeoff": pass
        elif command == "land": pass
        elif command == "pulse": pass
        elif command == "airlift": pass
        elif command == "survey": pass
        elif command == "bomb": pass
        elif command == "health": pass
        elif command == "kill": pass
        else: print(errorMessages.get("bad"))
    elif len(rawCommand.split()) == 1:
        if rawCommand == "attack": pass
        elif rawCommand == "next":
            airPhase = False
            return
        elif rawCommand == "score": score()
        elif rawCommand == "help": helpText()
        elif rawCommand == "details": details()
        elif rawCommand == "quit": quitGame()
        else: 
            print(errorMessages.get("bad"))
            return
    else: 
        print(errorMessages.get("bad"))
        return
    commandNumber = commandNumber + 1
    airShell(team, targetTeam, teamTable, targetTeamTable)

def shell(team, targetTeam, teamTable, targetTeamTable):
    global airPhase
    global commandNumber
    if airPhase == True and airTheater == True: 
        airShell(team, targetTeam, teamTable, targetTeamTable)
        return
    prompt = str(round) + " ~ " + str(commandNumber) + " " + str(team) + " % "
    rawCommand = input(prompt)
    if len(rawCommand.split()) == 2:
        command, unit = rawCommand.split()
        if not unit in unitTable:
            print(errorMessages.get("unit"))
            return
        if unit in deadUnits and not command == "health":
            print(errorMessages.get("dead"))
            return
        if command in umpireCommands: umpireShell(command, unit, team, targetTeam, teamTable, targetTeamTable)
        elif command in agnosticCommands: agnosticShell(command, unit, team, targetTeam, teamTable, targetTeamTable)
        elif command in navyCommands: navyShell(command, unit, team, targetTeam, teamTable, targetTeamTable)
        elif command in armyCommands: airShell(command, unit, team, targetTeam, teamTable, targetTeamTable)
        else:
            print(errorMessages.get("bad"))
            return
    elif len(rawCommand.split()) == 1:
        if rawCommand == "attack": pass
        elif rawCommand == "score": score()
        elif rawCommand == "turn": turn()
        elif rawCommand == "quit": quitGame()
        elif rawCommand == "help": helpText()
        elif rawCommand == "details": details()
        else: print(errorMessages.get("bad"))
    else: 
        print(errorMessages.get("bad"))
        return
    commandNumber = commandNumber + 1

while True:
    while (round % 2) != 0: 
        shell(firstTeam, secondTeam, firstTeamTable, secondTeamTable)
    while (round % 2) == 0:  
        shell(secondTeam, firstTeam, secondTeamTable, firstTeamTable)