import random
import os
from manpages import * 
from coralsea import *

round = 1
usedUnits = []
immobileUnits = []
deadUnits = []
commandNumber = 1
secrets = ""
hiddenUnits = []
alreadyDropped = []

def move(unit, unitType, team):
    global immobileUnits
    global usedUnits
    if unit in immobileUnits:
        print("Immovable.")
        return
    if unitType in headingChange: print("Unit cannot exceed its maximum heading change.")
    if not unitType in moveAndFire: usedUnits.append(unit)
    immobileUnits.append(unit)

def heading(unit, unitType, team):
    global immobileUnits
    global usedUnits
    if not unitType in headingChange:
        print("Heading change not required.")
        return
    if unit in immobileUnits:
        print("Immovable.")
        return
    if not unitType in moveAndFire: usedUnits.append(unit)
    immobileUnits.append(unit)

def hide(unit, unitType, team):
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

def reveal(unit, unitType, team):
    global hiddenUnits
    if not unit in hiddenUnits:
        print("Not hidden.")
        return
    hiddenUnits.remove(unit)

def spy(unit, unitType, team):
    global usedUnits
    if not unitType in searchable:
        print("Cannot search.")
        return
    searchEffectiveness = random.randrange(1,7)
    if searchEffectiveness == 6:
        print("Good information.")
        details()
    elif searchEffectiveness == 1:
        print("Bad information.")
        details()
    else: print("No information.")
    usedUnits.append(unit)

def fire(unit, unitType, team):
    global immobileUnits
    global usedUnits
    global deadUnits
    global hiddenUnits
    global firstDamage
    global secondDamage
    if not unitType in fireTable:
        print("Cannot attack.")
        return
    if unit in hiddenUnits:
        print("Unit revealed.")
        reveal(unit, unitType)
    maximum = fireTable.get(unitType) + 1
    damageDealt = random.randrange(1,maximum)
    if team == firstTeam: 
        firstDamage = firstDamage + damageDealt
        print(firstTeam, "deal", damageDealt, "damage.")
    elif team == secondTeam:
        secondDamage = secondDamage + damageDealt
        print(secondTeam, "deal", damageDealt, "damage.")
    print("Manually enter any dead units using the manual(kill) command.")
    usedUnits.append(unit)
    immobileUnits.append(unit)

def build(unit, unitType, team):
    global immobileUnits
    global usedUnits
    if not unitType in buildTable:
        print("Cannot build.")
        return
    maximum = buildTable.get(unitType) + 1
    fortification = random.randrange(1,maximum)
    print("Fortification of strength", fortification, "built.")
    immobileUnits.append(unit)
    usedUnits.append(unit)

def torpedo(unit, unitType, team):
    global usedUnits
    global immobileUnits
    global firstDamage
    global secondDamage
    if team != firstTeam and team != secondTeam:
        print("No such team.")
        return
    if not unitType in torpedoable:
        print("Cannot launch torpedoes.")
        return
    torpedoEffectiveness = random.randrange(1,7)
    if torpedoEffectiveness == 6:
        print("Ship sunk.")
        manual("kill")
    else:
        if team == firstTeam: 
            firstDamage = firstDamage + torpedoEffectiveness
            print(firstTeam, "deal", torpedoEffectiveness, "damage.")
        elif team == secondTeam:
            secondDamage = secondDamage + torpedoEffectiveness
            print(secondTeam, "deal", torpedoEffectiveness, "damage.")
        print("Manually enter any dead units using the manual(kill) command.")
        print("Call defend() function if relevant.")
    usedUnits.append(unit)
    immobileUnits.append(unit)

def sortie(unit, unitType, team):
    global usedUnits
    global immobileUnits
    global firstDamage
    global secondDamage
    if not unitType in sortieTable:
        print("Cannot launch sorties.")
        return
    if unit in hiddenUnits:
        print("Unit revealed.")
        reveal(unit, unitType)
    maximum = sortieTable.get(unitType) + 1
    damageDealt = random.randrange(1,maximum)
    if team == firstTeam: 
        firstDamage = firstDamage + damageDealt
        print(firstTeam, "deal", damageDealt, "damage.")
    elif team == secondTeam:
        secondDamage = secondDamage + damageDealt
        print(secondTeam, "deal", damageDealt, "damage.")
    print("Manually enter any dead units using the manual(kill) command.")
    print("Sorties can be defended against with the defend() command.")
    usedUnits.append(unit)
    immobileUnits.append(unit)

def depthcharge(unit, unitType, team):
    global immobileUnits
    global usedUnits
    global alreadyDropped
    global firstDamage
    global secondDamage
    if not unitType in depthchargeable:
        print("Cannot drop depth charges.")
        return
    if unit in alreadyDropped:
        print("Already dropped depth charges.")
        return
    chargeEffectiveness = random.randrange(1,7)
    if chargeEffectiveness == 6:
        print("Submarine sunk.")
        if team == firstTeam: firstDamage = firstDamage + 1
        elif team == secondTeam: secondDamage = secondDamage + 1
        manual("kill")
    elif chargeEffectiveness == 5:
        print("Submarine disabled.")
        disabled = input("Submarine unit disabled: ")
        immobileUnits.append(disabled)
        usedUnits.append(disabled)
    immobileUnits.append(unit)

def man(argument):
    manpage = str(argument)
    if os.name == "nt": path = "manpages\\" + manpage
    elif os.name == "posix": path = "manpages/" + manpage
    else: 
        print("Unknown operating system.")
        return
    file = open(path, "r")
    for line in file:
        print(file.read())

def attack(team):
    global immobileUnits
    global usedUnits
    global deadUnits
    global hiddenUnits
    global firstDamage
    global secondDamage
    attackPhase = True
    defensePhase = False
    totalAttackDamage = 0
    totalDefenseDamage = 0
    willQuit = False
    while attackPhase == True:
        prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + team + "][attack]% "
        attackCommand = input(prompt)
        argsInAttackCommand = attackCommand.split()
        if len(argsInAttackCommand) == 1:
            if attackCommand == "help":
                print("Syntax: [unit] [unitType]")
                print("'quit' to exit without saving, 'defend' to proceed to defense phase.")
            elif attackCommand == "quit": 
                attackPhase = False
                defensePhase = False
                willQuit = True
            elif attackCommand == "defend":
                attackPhase = False
                defensePhase = True
            else: print("Unknown command.")
        elif len(argsInAttackCommand) == 2:
            unit, unitType = attackCommand.split()
            try:
                if unit in hiddenUnits: reveal(unit, unitType, team)
                maximum = attackTable.get(unitType) + 1
                attackDamage = random.randrange(1, maximum)
                totalAttackDamage = totalAttackDamage + attackDamage
                print("Damage dealt:", attackDamage)
                print("Total damage dealt:", totalAttackDamage)
                usedUnits.append(unit)
                immobileUnits.append(unit)
            except: print("No such unit or unit type.")
        else: print("Too many arguments.")
    while defensePhase == True:
        prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + team + "][defense]% "
        defenseCommand = input(prompt)
        argsInDefendCommand = defenseCommand.split()
        if len(argsInDefendCommand) == 1:
            if defenseCommand == "help":
                print("Syntax: [unit] [unitType]")
                print("'quit' to exit without saving, 'save' to save to gamestate.")
            elif defenseCommand == "quit":
                defensePhase = False
                willQuit = True
            elif defenseCommand == "save": defensePhase = False
            else: print("Unknown command.")
        elif len(argsInDefendCommand) == 2:
            unit, unitType = defenseCommand.split()
            try:
                if unit in hiddenUnits: reveal(unit, unitType, team)
                maximum = attackTable.get(unitType) + 1
                defenseDamage = random.randrange(1, maximum)
                totalDefenseDamage = totalDefenseDamage + defenseDamage
                print("Defense damage dealt: ", defenseDamage)
                print("Total defense damage dealt: ", totalDefenseDamage)
                usedUnits.append(unit)
                immobileUnits.append(unit)
            except: print("No such unit or unit type.")
        else: print("Too many arguments.")
    if willQuit == True: return
    if totalAttackDamage > totalDefenseDamage: damageDealt = totalAttackDamage - totalDefenseDamage
    else: damageDealt = 0
    if team == firstTeam:
        firstDamage = firstDamage + damageDealt
        print(firstTeam, "deal", damageDealt, "damage.")
    elif team == secondTeam:
        secondDamage = secondDamage + damageDealt
        print(secondTeam, "deal", damageDealt, "damage.")
    print("If any units were killed in the exchange, call manual(kill).")

def getCommand(rawCommand, team):
    argsInCommand = rawCommand.split()
    if len(argsInCommand) == 4:
        command, unit, unitType = rawCommand.split()
        if command in validCommands:
            if unit in deadUnits:
                print("Dead.")
                return
            elif unit in usedUnits:
                print("Used.")
                return
            if command == "info": 
                info(unitType)
                if unit in deadUnits: print("Dead.")
                if unit in immobileUnits: print("Immovable this turn.")
                if unit in usedUnits: print("Unusable this turn.")
                if unit in hiddenUnits: print("Hidden.")
            else: globals()[command](unit, unitType, team)
        else: print("Unknown command or bad syntax.")
    elif len(argsInCommand) == 2:
        command, argument = rawCommand.split()
        twoWordCommands = ["man", "manual"]
        if command == "manual": manual(argument, team)
        elif command in twoWordCommands: globals()[command](argument)
        else: print("Unknown command or bad syntax.")
    elif len(argsInCommand) == 1:
        oneWordCommands = ["score", "turn", "quit", "help", "attack", "details"]
        if rawCommand in oneWordCommands:
            if rawCommand == "quit": quitGame()
            elif rawCommand == "help": helpText()
            elif rawCommand == "attack": attack(team)
            else: globals()[rawCommand]()
        else: print("Unknown command or bad syntax.")
    else:
        print("A command requires 1 to 3 words.")

def manual(argument, team):
    global firstDamage
    global secondDamage
    global deadUnits
    global immobileUnits
    if argument == "help": print("Arguments for manual() function: health, kill, freeze.")
    elif argument == "health":
        score()
        teamToChange = input(manualHelpPrompt)
        newValue = int(input("New health value: "))
        if teamToChange == "b": firstDamage = secondHealth - newValue
        else: secondDamage = firstHealth - newValue
    elif argument == "kill":
        namedUnit = input("Name of unit: ")
        currentValue = int(input("Current value of unit: "))
        deadUnits.append(namedUnit)
        if team == secondDamage: firstDamage = firstDamage + currentValue
        elif team == firstDamage: secondDamage = secondDamage + currentValue
    elif argument == "freeze":
        namedUnit = input("Name of unit: ")
        immobileUnits.append(namedUnit)
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

def details():
    print(secrets)
    
def turn():
    global round
    usedUnits.clear()
    immobileUnits.clear()
    round = round + 1

def quitGame():
    score()
    quit()

def helpText():
    global validCommands
    global allUnitTypes
    print("turn, quit, man, help, details, score")
    print(*validCommands, sep = ", ")
    print(*allUnitTypes, sep = ", ")

while True:
    while (round % 2) != 0:
        prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + firstTeam + "]% "
        rawCommand = input(prompt)
        getCommand(rawCommand, firstTeam)
        commandNumber = commandNumber + 1
    while (round % 2) == 0:
        prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + secondTeam + "]% "
        rawCommand = input(prompt)
        getCommand(rawCommand, secondTeam)
        commandNumber = commandNumber + 1