# This is an annotated version of kriegsspiel.py. I removed all of the comments from the original and converted them here, since the comments were becoming long and burdensome.
# This version is NON-RUNNABLE. If you are opening this with Visual Studio or some other Python IDE, running it will not work. It is meant for research and documentation purposes only. Primarily, the reason that this is the case is because the functions are juggled around in order to make documentation easier. 
# Essentially, this program is divided into four sections: definitions and imports, the game loop and shell, meta-functions, and callable functions.

# Part I: Definitions and Imports

# I-a. Imports
import random # random.randrange() sed only by the evaluate() meta function to simulate rolling dice with a computer.
import os # os.name() used only by the man() callable function. See man() for more.
from nile import * # Most important import statement. Replace "nile" with the name of whatever gamefile you want to use. When doing this, move the gamefile from the gamefiles/ directory to the main one, alongside kriegsspiel.py. Notice that the ordinary "import module" statement is not used here like it is for the random and os modules. "from module import *" is generally not recommened, since it is a security flaw, but in this case, we are only importing a single Python file, full of definitions, created by the user. However, since this is a security hole, I recommend that anyone using this program check a gamefile downloaded from another user.

# I-b. Definitions
round = 1 # Sets the round equal to 1 initially, so that the shell has a number to work with before turn() is called.
usedUnits = [] # All lists defined in this list are to contain strings, containing the names of various units. This list contains units that have already been used in the current turn. It is cleared every turn.
immobileUnits = [] # Units that have already moved or taken an action which prevents it from moving are contained in this list, which is again cleared at the end of every turn.
hiddenUnits = [] # Units that are hidden are stored here. hide() appends units to this list, reveal() removes them from it.
alreadyDropped = [] # depthcharge() cannot only be called once per unit, but a unit that drops depth charges can also perform other commands, so another list needs to be added exclusively for the depthcharge() function to use. Cleared every turn.
defendingUnits = [] # In fire() and attack(), a list of units defending needs to be looped through to ensure clean attribution of damages.
doubleImmobileUnits = [] # depthcharge() can immobilize a submarine during the next turn. As such, another list needs to exist to ensure that units are re-added to the immobileUnits list.
deadUnits = [] # While not strictly required, the deadUnits list is included for ease of searching
commandNumber = 1 # Sets the commandNumber to 1 intially, so that the shell has a number to work with at the beginning of the game
secrets = "" # Empty string originally, added to when hide() is called, so that the umpire can keep track of the secret locations.
oneWordCommands = {"score":"score", "turn":"turn", "quit":"quitGame", "help":"helpText", "attack":"attack", "details":"details"}

# Part II: Game Loop and Shell

# II-a. Main game loop
while True: # Loop runs permanently, until the quitGame() function is called
   while (round % 2) != 0: shell(firstTeam, secondTeam, secondTeamTable, firstTeamTable)
   while (round % 2) == 0: shell(secondTeam, firstTeam, firstTeamTable, secondTeamTable)

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
        if rawCommand == "attack": attack(team, targetTeam, targetTeamTable, teamTable) 
        else:
            try: globals()[oneWordCommands.get(rawCommand)]()
            except: 
                throwError("bad")
                return
    commandNumber = commandNumber + 1

# Part III: Meta-functions

def throwError(function):
    if function == "arguments": errorMessage = "Too many arguments for command. Type 'man' [command] for information."
    elif function == "bad": errorMessage = "Bad command. Type 'help' for assistance."
    elif function == "os": errorMessage = "Unknown operating system."
    elif function == "team": errorMessage = "That unit does not belong to you, or it does not exist."
    elif function == "available": errorMessage = "That unit is currently unavailable."
    elif function == "function": errorMessage = "That function is unavailable to this unit."
    elif function == "heading": errorMessage = "Unit cannot exceed its maximum heading change."
    elif function == "dead": errorMessage = "Unit is dead."
    print(errorMessage)

def update():
    global firstHealth
    global secondHealth
    global firstTeamTable
    global secondTeamTable
    firstHealth = sum(firstTeamTable.values())
    secondHealth = sum(secondTeamTable.values())

def score():
    update()
    firstPercent = firstHealth / firstHealthTotal * 100
    secondPercent = secondHealth / secondHealthTotal * 100
    print(firstTeam, "total health:", firstHealth, "or", firstPercent, "%")
    print(secondTeam, "total health:", secondHealth, "or", secondPercent, "%")

def changeList(unit, list, command):
    global usedUnits
    global immobileUnits
    global hiddenUnits
    global alreadyDropped
    global defendingUnits
    global deadUnits
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
    if unit in deadUnits:
        throwError("dead")
        return
    if unit in hiddenUnits: 
        try: reveal(unit, unitType, team, targetTeam, targetTeamTable, teamTable)
        except: pass
    if table.get(unitType) == None: return
    maximum = table.get(unitType) + 1
    damage = random.randrange(1, maximum)
    return damage

# Part IV: Callable Functions

def kill(unit, unitType, team, targetTeam, targetTeamTable, teamTable):
    global firstTeamTable
    global secondTeamTable
    teamTable[unit] = 0
    changeList(unit, deadUnits, "append")
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
    if unit in deadUnits:
        throwError("dead")
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
    if unitType in hideTable:
        prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + team + "][hide]% "
        location = input(prompt)
        newSecret = unit + " " + location
        secrets = secrets + ", " + newSecret
        changeList(unit, hiddenUnits, "append")
    else: 
        throwError("function")
        return

def reveal(unit, unitType, team, targetTeam, targetTeamTable, teamTable):
    global secrets
    global hiddenUnits
    if not unit in hiddenUnits:
        throwError("function")
        return
    if unitType in hideTable: hiddenUnits.remove(unit)
    else: throwError("function")

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
    if not unitType in fireTable:
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
    score()
    turn()

def build(unit, unitType, team, targetTeam, targetTeamTable, teamTable):
    global firstTeamTable
    global secondTeamTable
    fortification = evaluate(unit, unitType, team, targetTeam, targetTeamTable, teamTable, buildTable)
    if type(fortification) is int:
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
    score()

def sortie(unit, unitType, team, targetTeam, targetTeamTable, teamTable):
    global firstTeamTable
    global secondTeamTable
    if not unitType in sortieTable:
        throwError("function")
        return
    attackDamage = evaluate(unit, unitType, team, targetTeam, targetTeamTable, teamTable, sortieTable)
    if attackDamage == None:
        throwError("function")
        return
    prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + team + "][sortie]% "
    target = input(prompt)
    targetUnitType = unitTable.get(target)
    defenseDamage = evaluate(target, targetUnitType, targetTeam, targetTeam, targetTeamTable, targetTeamTable, sortieTable)
    if defenseDamage == None: defenseDamage = 0
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
        immobileUnits.append(target)
        print(target, "frozen.")
    elif effectiveness == None: return
    else: print("Missed.")
    changeList(unit, immobileUnits, "append")
    changeList(unit, alreadyDropped, "append")

def man(command, unitType, team, targetTeam, targetTeamTable, teamTable):
    if os.name == "nt": path = "manpage\\" + str(command)
    elif os.name == "posix": path = "manpages/" + str(command)
    else: throwError("os")
    file = open(path, "r")
    for line in file: print(file.read())

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
            defenseDamage = evaluate(command, unitType, targetTeam, targetTeam, targetTeamTable, targetTeamTable, attackTable)
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
    score()

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
    global validCommands
    global allUnitTypes
    print("turn, quit, man, help, details, score")
    print(*validCommands, sep = ", ")
    print(*allUnitTypes, sep = ", ")
    print("To learn more about any command, type 'man [command]'.")