import random
import os
from nile import *

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
oneWordCommands = {"score":"score", "turn":"turn", "quit":"quitGame", "help":"helpText", "attack":"attack", "details":"details"}
errorMessages = {"arguments":"Too many arguments for command. Type 'man' [command] for information.", "os":"Unknown operating system.", "bad":"Bad command. Type 'help' for assistance.", "team":"That unit does not belong to you, or it does not exist.", "available":"That unit is currently unavailable.", "function":"That function is unavailable to this unit.", "heading":"Unit cannot exceed its maximum heading change.", "dead":"Unit is dead.", "type":"No such unit type."}

# umpire functions: health, kill, freeze, disable, merge, split
# agnostic: move, hide, reveal, spy, fire, convert
# navy: heading, torpedo, sortie, depthcharge, load, disembark
# amry: build
# air: takeoff, land, pulse, airlift, survey, bomb

def score():
    update()
    firstPercent = firstHealth / firstHealthTotal * 100
    secondPercent = secondHealth / secondHealthTotal * 100
    print(firstTeam, "total health:", firstHealth, "or", firstPercent, "%")
    print(secondTeam, "total health:", secondHealth, "or", secondPercent, "%")

def freeze(unit, unitType, team, targetTeam, targetTeamTable, teamTable):
    changeList(unit, immobileUnits, "append")

def evaluate(unit, unitType, team, targetTeam, targetTeamTable, teamTable, table):
    global firstTeamTable
    global secondTeamTable
    if not unit in teamTable:
        print(errorMessages.get("team"))
        return
    if unit in immobileUnits or unit in usedUnits:
        print(errorMessages.get("available"))
        return
    if unit in deadUnits:
        print(errorMessages.get("dead"))
        return
    if unit in hiddenUnits:
        try: reveal(unit, unitType, team, targetTeam, targetTeamTable, teamTable)
        except: pass
    if table.get(unitType) == None: return
    maximum = table.get(unitType) + 1
    damage = random.randrange(1, maximum)
    return damage

def turn():
    global round
    changeList(True, usedUnits, "clear")
    changeList(True, immobileUnits, "clear")
    changeList(True, alreadyDropped, "clear")
    for x in doubleImmobileUnits: changeList(x, immobileUnits, "append")
    changeList(True, doubleImmobileUnits, "clear")
    round = round + 1

def details():
    print("Secrets:")
    print(secrets)
    print("Hidden units:")
    print(*hiddenUnits, sep = ", ")
    score()

def attack(team, targetTeam, targetTeamTable, teamTable):
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
            attackDamage = evaluate(command, unitType, team, targetTeam, targetTeamTable, teamTable, attackTable)
            try: 
                totalAttackDamage = totalAttackDamage + attackDamage
                changeList(command, usedUnits, "append")
                if not command in moveAndFire: changeList(command, immobileUnits, "append")
            except: pass
            print("Damage dealt:", attackDamage)
            print("Total damage dealt:", totalAttackDamage)
        else: print(errorMessages.get("bad"))
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
            defenseDamage = evaluate(command, unitType, targetTeam, targetTeam, targetTeamTable, targetTeamTable, attackTable)
            try: 
                totalDefenseDamage = totalDefenseDamage + defenseDamage
                changeList(command, defendingUnits, "append")
            except: pass
            print("Defense dealt:", defenseDamage)
            print("Total defense dealt:", totalDefenseDamage)
            if totalDefenseDamage >= totalAttackDamage: defensePhase = False
        else: print(errorMessages.get("bad"))
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
        if oldHealth - perUnitDamage <= 0: 
            newHealth = 0
            print(x, "killed.")
        else: 
            newHealth = oldHealth - perUnitDamage
            print(x, "new health:", newHealth)
        targetTeamTable[x] = newHealth
    changeList(True, defendingUnits, "clear")
    score()

def health(unit, unitType, team, targetTeam, targetTeamTable, teamTable):
    global firstTeamTable
    global secondTeamTable
    if unit in firstTeamTable: relevantTable = firstTeamTable
    elif unit in secondTeamTable: relevantTable = secondTeamTable
    else:
        print(errorMessages.get("team"))
        return
    print("Current health: ", relevantTable.get(unit))
    newHealth = input("New health: ")
    if newHealth <= 0: kill(unit, unitType, team, targetTeam, targetTeamTable, relevantTable)
    else: relevantTable[unit] = int(newHealth)
    update()

def convert(unit, unitType, team, targetTeam, targetTeamTable, teamTable):
    global firstTeamTable
    global secondTeamTable
    global unitTable
    if unit in firstTeamTable: 
        relevantTable = firstTeamTable
    elif unit in secondTeamTable: relevantTable = secondTeamTable
    else:
        print(errorMessages.get("team"))
        return
    prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + team + "][convert]% "
    newUnitType = input(prompt)
    if not newUnitType in allUnitTypes:
        print(errorMessages.get("type"))
        return
    currentHealth = relevantTable.get(unit)
    maximumHealth = healthTable.get(newUnitType)
    if maximumHealth < currentHealth: newHealth = maximumHealth
    else: newHealth = currentHealth
    relevantTable[unit] = currentHealth
    unitTable[unit] = newUnitType
    if unit in hiddenUnits and not newUnitType in hideTable: reveal(unit, unitType, team, targetTeam, targetTeamTable, teamTable)

def info(unit, unitType, team, targetTeam, targetTeamTable, teamTable):
    if not unit in unitTable:
        print(errorMessages.get("team"))
        return
    print("Unit type:", unitTable.get(unit))
    print("Maximum health:", healthTable.get(unitType))
    if unit in firstTeamTable: 
        owner = firstTeam
        print("Current health:", firstTeamTable.get(unit))
        print("Owner:", firstTeam)
    else:
        owner = secondTeam
        print("Current health:", secondTeamTable.get(unit))
        print("Owner:", secondTeam)
    print("Movement:", movementTable.get(unitType))
    print("Attack:", attackTable.get(unitType))
    print("Build:", buildTable.get(unitType))
    print("Sortie:", sortieTable.get(unitType))
    print("Sortie defense:", sortieDefenseTable.get(unitType))
    print("Depth charge:", depthchargeTable.get(unitType))
    if unitType in spyTable: print("Can search.")
    if unitType in hideTable: print("Can hide.")
    if unitType in moveAndFire: print("Can move and fire in the same turn.")
    if unitType in torpedoTable: print("Can fire torpedoes.")
    if unitType in headingTable: print("Heading change required.")
    if unit in immobileUnits: print("Immovable this turn.")
    if unit in usedUnits: print("Unusable this turn.")
    if unit in hiddenUnits: print("Hidden.")
    
def quitGame():
    score()
    quit()

def helpText():
    print("turn, quit, help, details, attack, score")
    print(*validCommands, sep = ", ")
    print(*allUnitTypes, sep = ", ")
    print("To learn more about any command, type 'man [command]'.")

def shell(team, targetTeam, targetTeamTable, teamTable):
    global commandNumber
    prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + team + "]% "
    rawCommand = input(prompt)
    if len(rawCommand.split()) > 2: 
        print(errorMessages.get("arguments"))
        return
    elif len(rawCommand.split()) == 2:
        command, unit = rawCommand.split()
        unitType = unitTable.get(unit)
        if command in validCommands: 
            globals()[command](unit, unitType, team, targetTeam, targetTeamTable, teamTable)
            if command == "man": pass
            else:
                if unitTable.get(unit) == None:
                    print(errorMessages.get("team"))
                    return
        else: 
            print(errorMessages.get("bad"))
            return
    else:
        if rawCommand == "attack": attack(team, targetTeam, targetTeamTable, teamTable) 
        else:
            try: globals()[oneWordCommands.get(rawCommand)]()
            except: 
                print(errorMessages.get("bad"))
                return
    commandNumber = commandNumber + 1

while True:
    while (round % 2) != 0: shell(firstTeam, secondTeam, secondTeamTable, firstTeamTable)
    while (round % 2) == 0: shell(secondTeam, firstTeam, firstTeamTable, secondTeamTable)