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
defendingUnits = []

def throwError(function):
    if function == "arguments": errorMessage = "Too many arguments for command. Type 'man' [command] for information."
    elif function == "bad": errorMessage = "Bad command. Type 'help' for assistance."
    elif function == "os": errorMessage = "Unknown operating system."
    elif function == "team": errorMessage = "That unit does not belong to you."
    elif function == "available": errorMessage = "That unit is currently unavailable."
    elif function == "function": errorMessage = "That function is unavailable to this unit."
    print(errorMessage)

def score():
    firstPercent = firstHealth / firstHealthTotal * 100
    secondPercent = secondHealth / secondHealthTotal * 100
    print(firstTeam, "total health:", firstHealth, "or", firstPercent, "%")
    print(secondTeam, "total health:", secondHealth, "or", secondPercent, "%")

def calculateDamage(unit, unitType, team, table):
    global firstTeamTable
    global secondTeamTable
    if team == firstTeam: teamTable = firstTeamTable
    if team == secondTeam: teamTable = secondTeamTable
    if not unit in teamTable:
        throwError("team")
        return
    if unit in immobileUnits or unit in usedUnits:
        throwError("available")
        return
    if unit in hiddenUnits: reveal(unit, unitType, team)
    maximum = table.get(unitType) + 1
    damage = random.randrange(1, maximum)
    return damage

def kill(unit, unitType, team):
    global firstHealth
    global secondHealth
    global firstTeamTable
    global secondTeamTable
    if team == firstTeam: 
        firstTeamTable[unit] = 0
        firstHealth = sum(firstTeamTable.values())
    else: 
        secondTeamTable[unit] = 0
        secondHealth = sum(secondTeamTable.values())

def freeze(unit, unitType, team):
    global immobileUnits
    immobileUnits.append(unit)

def turn():
    global round
    usedUnits.clear()
    immobileUnits.clear()
    alreadyDropped.clear()
    round = round + 1

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
    global firstHealth
    global secondHealth
    global firstTeamTable
    global secondTeamTable
    global defendingUnits
    global usedUnits
    defensePhase = True
    willQuit = False
    if team == firstTeam:
        targetTeam = secondTeam
        targetTeamTable = secondTeamTable
    else:
        targetTeam = firstTeam
        targetTeamTable = firstTeamTable
    while defensePhase == True:
        prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + team + "][fire]% "
        command = input(prompt)
        if command == "help": print("Enter a named unit, 'save' to save changes to gamestate, or 'quit' to exit without saving.")
        elif command == "quit":
            defensePhase = False
            willQuit = True
        elif command == "save": defensePhase = False
        elif command in unitTable:
            try: defendingUnits.append(command)
            except: pass
        else: throwError("bad")
    if willQuit == True: return
    damage = calculateDamage(unit, unitType, team, fireTable)
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
    firstHealth = sum(firstTeamTable.values())
    secondHealth = sum(secondTeamTable.values())
    score()
    turn()

def build(unit, unitType, team):
    global immobileUnits
    global usedUnits
    global firstTeamTable
    global secondTeamTable
    fortification = calculateDamage(unit, unitType, team, buildTable)
    if int(fortification) == fortification:
        print("Fortification of strength", fortification, "built.")
        usedUnits.append(unit)
        immobileUnits.append(unit)
    else: return

def torpedo(unit, unitType, team):
    global usedUnits
    global immobileUnits
    global firstHealth
    global secondHealth
    global firstTeamTable
    global secondTeamTable
    if team == firstTeam:
        targetTeam = secondTeam
        targetTeamTable = secondTeamTable
    else:
        targetTeam = firstTeam
        targetTeamTable = firstTeamTable
    prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + team + "][torpedo]% "
    target = input(prompt)
    targetUnitType = unitTable.get(target)
    damage = calculateDamage(unit, unitType, team, torpedoTable)
    oldHealth = targetTeamTable.get(target)
    if damage == 6 or oldHealth - damage <= 0:
        print(target, "sunk.")
        kill(target)
    else:
        newHealth = oldHealth - damage
        print(target, "new health:", newHealth)
        targetTeamTable[target] = newHealth
    usedUnits.append(unit)
    immobileUnits.append(unit)
    firstHealth = sum(firstTeamTable.values())
    secondHealth = sum(secondTeamTable.values())
    score()

def sortie(unit, unitType, team):
    global usedUnits
    global immobileUnits
    global firstHealth
    global secondHealth
    global firstTeamTable
    global secondTeamTable
    if team == firstTeam: 
        targetTeam = secondTeam
        targetTeamTable = secondTeamTable
    else: 
        targetTeam = firstTeam
        targetTeamTable = firstTeamTable
    if not unitType in sortieTable:
        throwError("function")
        return
    prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + team + "][sortie]% "
    target = input(prompt)
    targetUnitType = unitTable.get(target)
    attackDamage = calculateDamage(unit, unitType, team, sortieTable)
    defenseDamage = calculateDamage(target, targetUnitType, targetTeam, sortieDefenseTable)
    if defenseDamage <= attackDamage:
        netDamage = attackDamage - defenseDamage
        oldHealth = targetTeamTable[target]
        if oldHealth - netDamage < 0: kill(target, targetUnitType, targetTeam)
        else: 
            newHealth = oldHealth - netDamage
            print(target, "new health:", newHealth)
            targetTeamTable[target] = newHealth
    else: print("Attack repelled by:", target)
    usedUnits.append(unit)
    immobileUnits.append(unit)
    firstHealth = sum(firstTeamTable.values())
    secondHealth = sum(secondTeamTable.values())
    score()

def depthcharge(unit, unitType, team):
    global alreadyDropped
    global immobileUnits
    if team == firstTeam: targetTeam = secondTeam
    else: targetTeam = firstTeam
    if not unitType in depthchargeTable:
        throwError("function")
        return
    if unit in alreadyDropped:
        throwError("available")
        return
    prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + team + "][depthcharge]% "
    target = input(prompt)
    targetUnitType = unitTable.get(target)
    effectiveness = calculateDamage(unit, unitType, team, depthchargeTable)
    if effectiveness == 6: 
        kill(target, targetUnitType, targetTeam)
        print(target, "sunk.")
    elif effectiveness == 5: 
        freeze(target, targetUnitType, targetTeam)
        print(target, "frozen.")
    else: print("Missed.")
    immobileUnits.append(unit)
    alreadyDropped.append(unit)

def man(command, arg2, arg3):
    if os.name == "nt": path = "manpage\\" + str(command)
    elif os.name == "posix": path = "manpages/" + str(command)
    else: throwError("os")
    file = open(path, "r")
    for line in file: print(file.read())

def attack(team):
    global firstHealth
    global secondHealth
    global firstTeamTable
    global secondTeamTable
    global defendingUnits
    global usedUnits
    attackPhase = True
    defensePhase = False
    willQuit = False
    totalAttackDamage = 0
    totalDefenseDamage = 0
    if team == firstTeam: 
        defendingTeam = secondTeam
        defenseTable = secondTeamTable
    else: 
        defendingTeam = firstTeam
        defenseTable = firstTeamTable
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
            attackDamage = calculateDamage(command, unitType, team, attackTable)
            try: 
                totalAttackDamage = totalAttackDamage + attackDamage
                usedUnits.append(command)
                if not command in moveAndFire: freeze(command)
            except: pass
            print("Damage dealt:", attackDamage)
            print("Total damage dealt:", totalAttackDamage)
        else: throwError("bad")
    while defensePhase == True:
        prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + defendingTeam + "][defend]% "
        command = input(prompt)
        if command == "help": print("Enter a named unit to defend, 'save' to save changes to gamestate, or 'quit' to exit without saving.")
        elif command == "quit":
            defensePhase = False
            willQuit = True
        elif command == "save": defensePhase = False
        elif command in unitTable:
            unitType = unitTable.get(command)
            defenseDamage = calculateDamage(command, unitType, defendingTeam, attackTable)
            try: 
                totalDefenseDamage = totalDefenseDamage + defenseDamage
                defendingUnits.append(command)
            except: pass
            print("Defense dealt:", defenseDamage)
            print("Total defense dealt:", totalDefenseDamage)
            if totalDefenseDamage >= totalAttackDamage: defensePhase = False
        else: throwError("bad")
    if willQuit == True: return
    if totalDefenseDamage >= totalAttackDamage:
        print("Attack repelled by", defendingTeam)
        return
    else:
        netDamage = totalAttackDamage - totalDefenseDamage
        print("Net damage:", netDamage)
        perUnitDamage = netDamage / len(defendingUnits)
        print("Damage per unit:", perUnitDamage)
        for x in defendingUnits:
            oldHealth = defenseTable.get(x)
            if oldHealth - perUnitDamage < 0: 
                newHealth = 0
                print(x, "killed.")
            else: 
                newHealth = oldHealth - perUnitDamage
                print(x, "new health:", newHealth)
            defenseTable[x] = newHealth
        firstHealth = sum(firstTeamTable.values())
        secondHealth = sum(secondTeamTable.values())
        score()
        turn()

def health(unit, unitType, team):
    global firstHealth
    global secondHealth
    global firstTeamTable
    global secondTeamTable
    if unit in firstTeamTable:
        print("Current health:", firstTeamTable.get(unit))
        newHealth = input("New health: ")
        firstTeamTable[unit] = int(newHealth)
        firstHealth = sum(firstTeamTable.values())
    else:
        print("Current health:", secondTeamTable.get(unit))
        newHealth = input("New health: ")
        secondTeamTable[unit] = int(newHealth)
        secondHealth = sum(secondTeamTable.values())

def details():
    print(secrets)

def info(unit, unitType, team):
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
    if unitType in searchable: print("Can search.")
    if unitType in hideable: print("Can hide.")
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
        if rawCommand == "attack": attack(team) 
        else:
            try: globals()[oneWordCommands.get(rawCommand)]()
            except: 
                throwError("bad")
                return
    commandNumber = commandNumber + 1

while True:
    while (round % 2) != 0: shell(firstTeam)
    while (round % 2) == 0: shell(secondTeam)