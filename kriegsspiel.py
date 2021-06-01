import random
import os
from brandywine import *

round = 1
usedUnits = []
immobileUnits = []
hiddenUnits = []
alreadyDropped = []
defendingUnits = []
commandNumber = 1
secrets = ""
oneWordCommands = {"score":"score", "turn":"turn", "quit":"quitGame", "help":"helpText", "attack":"attack", "details":"details"}

def throwError(function):
    if function == "arguments": errorMessage = "Too many arguments for command. Type 'man' [command] for information."
    elif function == "bad": errorMessage = "Bad command. Type 'help' for assistance."
    elif function == "os": errorMessage = "Unknown operating system."
    elif function == "team": errorMessage = "That unit does not belong to you."
    elif function == "available": errorMessage = "That unit is currently unavailable."
    elif function == "function": errorMessage = "That function is unavailable to this unit."
    elif function == "heading": errorMessage = "Unit cannot exceed its maximum heading change."
    print(errorMessage)

def score():
    firstPercent = firstHealth / firstHealthTotal * 100
    secondPercent = secondHealth / secondHealthTotal * 100
    print(firstTeam, "total health:", firstHealth, "or", firstPercent, "%")
    print(secondTeam, "total health:", secondHealth, "or", secondPercent, "%")

def update():
    global firstHealth
    global secondHealth
    global firstTeamTable
    global secondTeamTable
    firstHealth = sum(firstTeamTable.values())
    secondHealth = sum(secondTeamTable.values())

def changeList(unit, list, command):
    global usedUnits
    global immobileUnits
    global hiddenUnits
    global alreadyDropped
    global defendingUnits
    if command == "append": list.append(unit)
    elif command == "clear": list.clear()
    elif command == "remove": list.remove(unit)

def evaluate(unit, unitType, team, targetTeam, targetTeamTable, teamTable, table):
    global firstTeamTable
    global secondTeamTable
    if not unit in teamTable:
        throwError("team")
        return
    if unit in immobileUnits or unit in usedUnits:
        throwError("available")
        return
    if unit in hiddenUnits: reveal(unit, unitType, team, targetTeam, targetTeamTable, teamTable)
    maximum = table.get(unitType) + 1
    damage = random.randrange(1, maximum)
    return damage

def kill(unit, unitType, team, targetTeam, targetTeamTable, teamTable):
    global firstTeamTable
    global secondTeamTable
    teamTable[unit] = 0
    update()

def turn():
    global round
    changeList(True, usedUnits, "clear")
    changeList(True, immobileUnits, "clear")
    changeList(True, alreadyDropped, "clear")
    changeList(True, defendingUnits, "clear")
    round = round + 1

def details():
    print("Secrets:")
    print(secrets)
    print("Hidden units:")
    print(*hiddenUnits, sep = ", ")
    score()

def move(unit, unitType, team, targetTeam, targetTeamTable, teamTable):
    if unit in immobileUnits:
        throwError("function")
        return
    if unitType in headingTable: throwError("heading")
    if not unitType in moveAndFire: changeList(unit, usedUnits, "append")
    changeList(unit, immobileUnits, "append")

def heading(unit, unitType, team, targetTeam, targetTeamTable, teamTable):
    headingValue = evaluate(unit, unitType, team, targetTeam, targetTeamTable, teamTable, headingTable)
    if headingValue == 1: 
        changeList(unit, immobileUnits, "append")
        if not unitType in moveAndFire: changeList(unit, usedUnits, "append")
    else: return

def hide(unit, unitType, team, targetTeam, targetTeamTable, teamTable):
    global secrets
    hideValue = evaluate(unit, unitType, team, targetTeam, targetTeamTable, teamTable, hideTable)
    if hideValue == 1:
        prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + team + "][hide]% "
        location = input(prompt)
        newSecret = unit + " " + location
        secrets = secrets + ", " + newSecret
        changeList(unit, hiddenUnits, "append")
    else: return

def reveal(unit, unitType, team, targetTeam, targetTeamTable, teamTable):
    global secrets
    if not unit in hiddenUnits:
        throwError("function")
        return
    revealValue = evaluate(unit, unitType, team, targetTeam, targetTeamTable, teamTable, hideTable)
    if revealValue == 1:
        secrets = secrets + ", ", unit, "no longer hidden."
        changeList(unit, hiddenUnits, "remove")
    else: return

def spy(unit, unitType, team, targetTeam, targetTeamTable, teamTable):
    effectiveness = evaluate(unit, unitType, team, targetTeam, targetTeamTable, teamTable, spyTable)
    if effectiveness == 6: print("Good information.")
    elif effectiveness == 1: print("Bad information.")
    else: print("No information.")
    details()
    changeList(unit, usedUnits, "append")

def fire(unit, unitType, team, targetTeam, targetTeamTable, teamTable):
    global firstTeamTable
    global secondTeamTable
    defensePhase = True
    willQuit = False
    if not unit in fireTable:
        throwError("function")
        return
    while defensePhase == True:
        prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + team + "][fire]% "
        command = input(prompt)
        if command == "help": print("Enter a named unit, 'save' to save changes to gamestate, or 'quit' to exit without saving.")
        elif command == "quit":
            defensePhase = False
            willQuit = True
        elif command == "save": defensePhase = False
        elif command in unitTable:
            try: changeList(command, defendingUnits, "append")
            except: pass
        else: throwError("bad")
    if willQuit == True: return
    damage = evaluate(unit, unitType, team, targetTeam, targetTeamTable, teamTable, fireTable)
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
    update()
    score()
    turn()

def build(unit, unitType, team, targetTeam, targetTeamTable, teamTable):
    global firstTeamTable
    global secondTeamTable
    fortification = evaluate(unit, unitType, team, targetTeam, targetTeamTable, teamTable, buildTable)
    if int(fortification) == fortification:
        print("Fortification of strength", fortification, "built.")
        changeList(unit, usedUnits, "append")
        changeList(unit, immobileUnits, "append")
    else: return

def torpedo(unit, unitType, team, targetTeam, targetTeamTable, teamTable):
    global firstTeamTable
    global secondTeamTable
    prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + team + "][torpedo]% "
    target = input(prompt)
    targetUnitType = unitTable.get(target)
    damage = evaluate(unit, unitType, team, targetTeam, targetTeamTable, teamTable, torpedoTable)
    oldHealth = targetTeamTable.get(target)
    if damage == 6 or oldHealth - damage <= 0:
        print(target, "sunk.")
        kill(target, targetUnitType, targetTeam, team, targetTeamTable, targetTeamTable)
    else:
        newHealth = oldHealth - damage
        print(target, "new health:", newHealth)
        targetTeamTable[target] = newHealth
    changeList(unit, usedUnits, "append")
    changeList(unit, immobileUnits, "append")
    update()
    score()

def sortie(unit, unitType, team, targetTeam, targetTeamTable, teamTable):
    global firstTeamTable
    global secondTeamTable
    if not unitType in sortieTable:
        throwError("function")
        return
    prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + team + "][sortie]% "
    target = input(prompt)
    targetUnitType = unitTable.get(target)
    attackDamage = evaluate(unit, unitType, team, targetTeam, targetTeamTable, teamTable, sortieTable)
    defenseDamage = evaluate(target, targetUnitType, targetTeam, targetTeam, targetTeamTable, teamTable, sortieTable)
    if defenseDamage <= attackDamage:
        netDamage = attackDamage - defenseDamage
        oldHealth = targetTeamTable[target]
        if oldHealth - netDamage < 0: kill(target, targetUnitType, targetTeam, targetTeam, targetTeamTable, targetTeamTable)
        else: 
            newHealth = oldHealth - netDamage
            print(target, "new health:", newHealth)
            targetTeamTable[target] = newHealth
    else: print("Attack repelled by:", target)
    changeList(unit, usedUnits, "append")
    changeList(unit, immobileUnits, "append")
    update()
    score()

def depthcharge(unit, unitType, team, targetTeam, targetTeamTable, teamTable):
    if not unitType in depthchargeTable:
        throwError("function")
        return
    if unit in alreadyDropped:
        throwError("available")
        return
    prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + team + "][depthcharge]% "
    target = input(prompt)
    targetUnitType = unitTable.get(target)
    effectiveness = evaluate(unit, unitType, team, targetTeam, targetTeamTable, teamTable, depthchargeTable)
    if effectiveness == 6: 
        kill(target, targetUnitType, targetTeam, targetTeam, targetTeamTable, targetTeamTable)
        print(target, "sunk.")
    elif effectiveness == 5: 
        freeze(target, targetUnitType, targetTeam, targetTeam, targetTeamTable, targetTeamTable)
        print(target, "frozen.")
    else: print("Missed.")
    changeList(unit, immobileUnits, "append")
    changeList(unit, alreadyDropped, "append")

def man(command, unitType, team, targetTeam, targetTeamTable, teamTable):
    if os.name == "nt": path = "manpage\\" + str(command)
    elif os.name == "posix": path = "manpages/" + str(command)
    else: throwError("os")
    file = open(path, "r")
    for line in file: print(file.read())

def attack(team, targetTeam, targetTeamTable):
    global firstTeamTable
    global secondTeamTable
    attackPhase = True
    defensePhase = False
    willQuit = False
    totalAttackDamage = 0
    totalDefenseDamage = 0
    while attackPhase == True:
        prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + team + "][attack]% "
        command = input(prompt)
        if command == "help": print("Enter a named unit to attack, 'defend' to change to the defense phase, or 'quit' to exit without saving.")
        elif command == "quit":
            attackPhase = False
            defensePhase = False
            willQuit = True
        elif command == "defend":
            attackPhase = False
            defensePhase = True
        elif command in unitTable:
            unitType = unitTable.get(command)
            attackDamage = evaluate(command, unitType, team, targetTeam, targetTeamTable, targetTeamTable, attackTable)
            try: 
                totalAttackDamage = totalAttackDamage + attackDamage
                changeList(command, usedUnits, "append")
                if not command in moveAndFire: changeList(command, immobileUnits, "append")
            except: pass
            print("Damage dealt:", attackDamage)
            print("Total damage dealt:", totalAttackDamage)
        else: throwError("bad")
    while defensePhase == True:
        prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + targetTeam + "][defend]% "
        command = input(prompt)
        if command == "help": print("Enter a named unit to defend, 'save' to save changes to gamestate, or 'quit' to exit without saving.")
        elif command == "quit":
            defensePhase = False
            willQuit = True
        elif command == "save": defensePhase = False
        elif command in unitTable:
            unitType = unitTable.get(command)
            defenseDamage = evaluate(command, unitType, targetTeam, targetTeamTable, targetTeamTable, attackTable)
            try: 
                totalDefenseDamage = totalDefenseDamage + defenseDamage
                changeList(command, defendingUnits, "append")
            except: pass
            print("Defense dealt:", defenseDamage)
            print("Total defense dealt:", totalDefenseDamage)
            if totalDefenseDamage >= totalAttackDamage: defensePhase = False
        else: throwError("bad")
    if willQuit == True: return
    if totalDefenseDamage >= totalAttackDamage:
        print("Attack repelled by", targetTeam)
        return
    netDamage = totalAttackDamage - totalDefenseDamage
    print("Net damage:", netDamage)
    perUnitDamage = netDamage / len(defendingUnits)
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
    update()
    score()
    turn()

def health(unit, unitType, team, targetTeam, targetTeamTable, teamTable):
    global firstTeamTable
    global secondTeamTable
    if unit in firstTeamTable:
        print("Current health:", firstTeamTable.get(unit))
        newHealth = input("New health: ")
        firstTeamTable[unit] = int(newHealth)
    else:
        print("Current health:", secondTeamTable.get(unit))
        newHealth = input("New health: ")
        secondTeamTable[unit] = int(newHealth)
    update()

def info(unit, unitType, team, targetTeam, targetTeamTable, teamTable):
    print("Unit type: ", unitTable.get(unit))
    print("Maximum health: ", healthTable.get(unitType))
    if unit in firstTeamTable: 
        owner = firstTeam
        print("Current health: ", firstTeamTable.get(unit))
        print("Owner: ", firstTeam)
    else: 
        owner = secondTeam
        print("Current health: ", secondTeamTable.get(unit))
        print("Owner: ", secondTeam)
    print("Movement: ", movementTable.get(unitType))
    print("Attack: ", attackTable.get(unitType))
    print("Build: ", buildTable.get(unitType))
    if unitType in spyTable: print("Can search.")
    if unitType in hideTable: print("Can hide.")
    if unitType in moveAndFire: print("Can move and fire in the same turn.")
    if unit in immobileUnits: print("Immovable this turn.")
    if unit in usedUnits: print("Unusable this turn.")
    if unit in hiddenUnits: print("Hidden.")

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

def shell(team, targetTeam, targetTeamTable, teamTable):
    global commandNumber
    prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + team + "]% "
    rawCommand = input(prompt)
    if len(rawCommand.split()) > 2: 
        throwError("arguments")
        return
    elif len(rawCommand.split()) == 2:
        command, unit = rawCommand.split()
        unitType = unitTable.get(unit)
        if command in validCommands: globals()[command](unit, unitType, team, targetTeam, targetTeamTable, teamTable)
        else: 
            throwError("bad")
            return
    else:
        if rawCommand == "attack": attack(team, targetTeam, targetTeamTable) 
        else:
            try: globals()[oneWordCommands.get(rawCommand)]()
            except: 
                throwError("bad")
                return
    commandNumber = commandNumber + 1

while True:
    while (round % 2) != 0: shell(firstTeam, secondTeam, secondTeamTable, firstTeamTable)
    while (round % 2) == 0: shell(secondTeam, firstTeam, firstTeamTable, secondTeamTable)