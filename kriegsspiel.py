import random
from manpages import * 
from coralsea import * # Gamefile import

# Global variables and lists
warPhase = True
round = 1
usedUnits = []
immobileUnits = []
deadUnits = []
commandNumber = 1
secrets = ""
hiddenUnits = []
alreadyDropped = []

# Functions
def move(unit, unitType):
    global immobileUnits
    global usedUnits
    if unit in immobileUnits:
        print("Immovable.")
        return
    if unitType in headingChange: print("Unit cannot exceed its maximum heading change.")
    if not unitType in moveAndFire: usedUnits.append(unit)
    immobileUnits.append(unit)

def heading(unit, unitType):
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

def attack(unit, unitType):
    global immobileUnits
    global usedUnits
    global deadUnits
    global hiddenUnits
    global firstDamage
    global secondDamage
    if not unitType in attackable:
        print("Cannot attack.")
        return
    if unit in hiddenUnits:
        print("Unit revealed.")
        reveal(unit, unitType)
    if unitType in attack4: maximum = 5
    elif unitType in attack6: maximum = 7
    elif unitType in attack8: maximum = 9
    elif unitType in attack12: maximum = 13
    elif unitType in attack16: maximum = 17
    elif unitType in attack20: maximum = 21
    elif unitType in attack24: maximum = 25
    damageDealt = random.randrange(1,maximum)
    owner = input(ownerPrompt)
    if owner == "a": 
        firstDamage = firstDamage + damageDealt
        print(firstTeam, "deal", damageDealt, "damage.")
    else: 
        secondDamage = secondDamage + damageDealt
        print(secondTeam, "deal", damageDealt, "damage.")
    print("Manually enter any dead units using the manual(kill) command.")
    print("Call defend() function if relevant.")
    usedUnits.append(unit)
    immobileUnits.append(unit)

def defend(unit, unitType):
    global firstDamage
    global secondDamage
    if not unitType in attackable:
        print("Cannot defend.")
        return
    if unitType in attack4: maximum = 5
    elif unitType in attack12: maximum = 13
    elif unitType in attack20: maximum = 21
    damageDealt = random.randrange(1,maximum)
    owner = input(ownerPrompt)
    if owner == "a":
        secondDamage = secondDamage - damageDealt
        print(firstTeam, "defends for", damageDealt, "damage.")
    else:
        firstDamage = firstDamage - damageDealt
        print(secondTeam, "defends for", damageDealt, "damage.")

def fire(unit, unitType):
    global immobileUnits
    global usedUnits
    global deadUnits
    global hiddenUnits
    global firstDamage
    global secondDamage
    if not unitType in fireable:
        print("Cannot attack.")
        return
    if unit in hiddenUnits:
        print("Unit revealed.")
        reveal(unit, unitType)
    if unitType in fire8: maximum = 9
    elif unitType in fire10: maximum = 11
    elif unitType in fire12: maximum = 13
    elif unitType in fire16: maximum = 17
    elif unitType in fire20: maximum = 21
    damageDealt = random.randrange(1,maximum)
    owner = input(ownerPrompt)
    if owner == "a": 
        firstDamage = firstDamage + damageDealt
        print(firstTeam, "deal", damageDealt, "damage.")
    else: 
        secondDamage = secondDamage + damageDealt
        print(secondTeam, "deal", damageDealt, "damage.")
    print("Manually enter any dead units using the manual(kill) command.")
    usedUnits.append(unit)
    immobileUnits.append(unit)

def build(unit, unitType):
    global immobileUnits
    global usedUnits
    if not unitType in buildable:
        print("Cannot build.")
        return
    if unitType in build4: print("Fortification of strength", random.randrange(1,5), "built.")
    elif unitType in build8: print("Fortification of strength", random.randrange(1,9), "built.")
    immobileUnits.append(unit)
    usedUnits.append(unit)

def hide(unit, unitType):
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

def reveal(unit, unitType):
    global hiddenUnits
    if not unit in hiddenUnits:
        print("Not hidden.")
        return
    hiddenUnits.remove(unit)

def spy(unit, unitType):
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

def torpedo(unit, unitType):
    global usedUnits
    global immobileUnits
    global firstDamage
    global secondDamage
    if not unitType in torpedoable:
        print("Cannot launch torpedoes.")
        return
    torpedoEffectiveness = random.randrange(1,7)
    if torpedoEffectiveness == 6:
        print("Ship sunk.")
        manual(kill)
    else:
        owner = input(ownerPrompt)
        if owner == "a": 
            firstDamage = firstDamage + torpedoEffectiveness
            print(firstTeam, "deal", torpedoEffectiveness, "damage.")
        else: 
            secondDamage = secondDamage + torpedoEffectiveness
            print(secondTeam, "deal", torpedoEffectiveness, "damage.")
        print("Manually enter any dead units using the manual(kill) command.")
        print("Call defend() function if relevant.")
    usedUnits.append(unit)
    immobileUnits.append(unit)

def sortie(unit, unitType):
    global usedUnits
    global immobileUnits
    global firstDamage
    global secondDamage
    if not unitType in sortieable:
        print("Cannot launch sorties.")
        return
    if unit in hiddenUnits:
        print("Unit revealed.")
        reveal(unit, unitType)
    if unitType in sortie8: maximum = 9
    damageDealt = random.randrange(1,maximum)
    owner = input(ownerPrompt)
    if owner == "a": 
        firstDamage = firstDamage + damageDealt
        print(firstTeam, "deal", damageDealt, "damage.")
    else: 
        secondDamage = secondDamage + damageDealt
        print(secondTeam, "deal", damageDealt, "damage.")
    print("Manually enter any dead units using the manual(kill) command.")
    print("Sorties can be defended against with the defend() command.")
    usedUnits.append(unit)
    immobileUnits.append(unit)

def depthcharge(unit, unitType):
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
        owner = input(ownerPrompt)
        if owner == "a": firstDamage = firstDamage + 1
        else: secondDamage = secondDamage + 1
        manual(kill)
    elif chargeEffectiveness == 5:
        print("Submarine disabled.")
        disabled = input("Submarine unit disabled: ")
        immobileUnits.append(disabled)
        usedUnits.append(disabled)
    immobileUnits.append(unit)

# Universal functions
def man(argument):
    if argument == "manual": print(manManual)
    elif argument == "man": print(manMan)
    elif argument == "score": print(manScore)
    elif argument == "turn": print(manTurn)
    elif argument == "quit": print(manQuit)
    elif argument == "help": print(manHelp)
    elif argument == "details": print(manDetails)
    elif argument == "move": print(manMove)
    elif argument == "attack": print(manAttack)
    elif argument == "defend": print(manDefend)
    elif argument == "fire": print(manFire)
    elif argument == "build": print(manBuild)
    elif argument == "hide": print(manHide)
    elif argument == "reveal": print(manReveal)
    elif argument == "spy": print(manSpy)
    elif argument == "heading": print(manHeading)
    elif argument == "torpedo": print(manTorpedo)
    elif argument == "sortie": print(manSortie)
    elif argument == "depthcharge": print(manDepthcharge)
    else: print("Bad command.")

def getCommand(command, unit, unitType):
    if unit in deadUnits:
        print("Dead.")
        return
    elif unit in usedUnits:
        print("Used.")
        return
    if command == "move": move(unit, unitType)
    elif command == "attack": attack(unit, unitType)
    elif command == "fire": fire(unit, unitType)
    elif command == "build": build(unit, unitType)
    elif command == "hide": hide(unit, unitType)
    elif command == "reveal": reveal(unit, unitType)
    elif command == "spy": spy(unit, unitType)
    elif command == "defend": defend(unit, unitType)
    elif command == "heading": heading(unit, unitType)
    elif command == "torpedo": torpedo(unit, unitType)
    elif command == "sortie": sortie(unit, unitType)
    elif command == "depthcharge": depthcharge(unit, unitType)
    elif command == "info": 
        info(unitType)
        if unit in deadUnits: print("Dead.")
        if unit in immobileUnits: print("Immovable this turn.")
        if unit in usedUnits: print("Unusable this turn.")
        if unit in hiddenUnits: print("Hidden.")
    else: print("Unknown command.")

def manual(argument):
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
        owner = input(ownerPrompt)
        if owner == "b": firstDamage = firstDamage + currentValue
        else: secondDamage = secondDamage + currentValue
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
    global warPhase
    score()
    warPhase = False

def helpText():
    print("turn, quit, man, help, details, score, new")
    print(*validCommands, sep = ", ")
    print(*allUnitTypes, sep = ", ")

# Game loop
while warPhase == True:
    prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "]% "
    rawCommand = input(prompt)
    argsInCommand = rawCommand.split()
    if len(argsInCommand) == 3:
        command, unit, unitType = rawCommand.split()
        if command in validCommands: getCommand(command, unit, unitType)
        else: print("Bad command, or wrong number of arguments for command. See help() or man(command) for help.")
    elif len(argsInCommand) == 2:
        command, argument = rawCommand.split()
        if command == "man": man(argument)
        elif command == "manual": manual(argument)
        else: print("Bad command, or wrong number of arguments for command. See help() or man(command) for help.")
    elif len(argsInCommand) == 1:
        if rawCommand == "score": score()
        elif rawCommand == "turn": turn()
        elif rawCommand == "quit": quitGame()
        elif rawCommand == "help": helpText()
        elif rawCommand == "details": details()
        else: print("Bad command, or wrong number of arguments for command. See help() or man(command) for help.")
    else:
        print("A command requires 1 to 3 words.")
    commandNumber = commandNumber + 1