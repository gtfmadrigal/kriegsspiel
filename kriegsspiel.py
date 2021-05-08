import random
from coralsea import *

# Global variables and lists
warPhase = True
round = 1
usedUnits = []
immobileUnits = []
deadUnits = []
commandNumber = 1
secrets = ""
hiddenUnits = []

# man() pages
manManual = """
manual(argument)
Meta-function

Allows the umpire to directly alter the attributes of units or teams in their entirety. Four arguments are allowed: "help", "health", "kill", and "freeze." Anything else yields an error.

--help: Lists the valid arguments.

--health:
1. Displays the score by calling the score() function.
2. Requests which team's health to alter.
3. Requests the new health value as an integer.
4. Alters the health value.

--kill:
1. Requests the name of the unit to kill.
2. Requests the current health value of the unit.
3. Places the unit in the deadUnits[] list.
4. Requests the unit's parent team.
5. Alters the overall health of the team accordingly.

--freeze:
1. Requests the name of the unit to freeze.
2. Places the unit in the immobileUnits[] list.
"""
manMan = """
man(argument)
Meta-function

Displays the informational page for the command passed to it.
"""
manScore = """
score()
Meta-function

Displays the damage dealt by each team and the percent remaining of their total initial health points.
"""
manTurn = """
turn()
Pseudo-function

Ends the current turn.

1. Clears the usedUnits[] list, making all units available for use again.
2. Clears the immobileUnits[] list, making all units movable again.
3. Increments the round.
"""
manQuit = """
quit()
Pseudo-function

Ends the game.

1. Calls score().
2. Sets warPhase to False, closing the primary game loop and exiting the script.
"""
manHelp = """
help()
Pseudo-function

Displays all valid commands

1. Displays the universal commands.
2. Displays the commands specified as available in the validCommands[] list.
"""
manDetails = """
details()
Meta-function

Displays relevant game information held in the secrets variable.
"""
manMove = """
move(unit, unitType)
Game function

Moves a unit.

1. Checks if unit is in the list immobileUnits[], in which case the function throws an error and quits.
2. Checks if unitType is not in the list moveAndFire[], in which case the unit is added to the list usedUnits[], preventing another command being given to that unit in the current turn.
3. Adds the unit to the immobileUnits[] list, preventing the unit from moving again in the current turn.
"""
manHeading = """
heading(unit, unitType)
Game function

Changes the heading of a unit.

1. Checks if unitType is required to change heading. If not, the function throws an error and quits.
2. Checks if unit is in the list immobileUnits[], in which case the function throws an error and quits.
3. Checks if unitType is not in the list moveAndFire[], in which case the unit is added to the list usedUnits[], preventing another command being given to that unit in the current turn.
4. Adds the unit to the immobileUnits[] list, preventing the unit from moving again in the current turn.
"""
manAttack = """
attack(unit, unitType)
Game function

Primary game function, causes a unit to attack another using its primary weapon, typically small arms.

1. Checks if the unitType has a primary weapon capability. If not, the function throws an error and quits.
2. Checks if the unit is hidden, in which case the reveal(unit, unitType) function is called.
3. Assigns a maximum value for the attack, based on the gamefile.
4. Determines the damage dealt by the attack, by randomly choosing a value from 1 to the maximum.
5. Requests the owner of the unit.
6. Deals the damage to the other team.
7. Adds the unit to the usedUnits[] list.
8. Adds the unit to the immobileUnits[] list.
9. Requests that the user calls the manual function to kill any units that are now dead, and the defend function.
"""
manDefend = """
defend(unit, unitType)
Game function

Reduces damage inflicted by an attack command. Effectively identical to the attack(unit, unitType) function, but inverted.
"""
manFire = """
fire(unit, unitType)
Game function

Inflicts damage based on the secondary weapon of a unit. Functionally similar to attack(unit, unitType). Cannot be defended.
"""
manBuild = """
build(unit, unitType)
Game function

Constructs a fortification.

1. Checks if unitType has building capacity. If not, the function throws an error and quits.
2. Assigns the maximum strength of the fortification based on the capabilities of the unitType.
3. Creates a fortification where the strength is a random number between 1 and the maximum.
4. Adds unit to immobileUnits[].
5. Adds unit to usedUnits[].
"""
manHide = """
hide(unit, unitType)
Game function

Hides unit from the enemy.

1. Checks if unitType has the ability to hide. If not, the function throws an error and quits.
2. Checks if unit is already hidden. If it is, the function throws an error and quits.
3. Adds unit to the hiddenUnits[] list.
4. Requests information about the location of the hidden unit.
5. Adds the information to the secrets variable.
"""
manReveal = """
reveal(unit, unitType)
Game function

Reveals a hidden unit.

1. Checks if unit is not hidden, in which case the function throws an error and quits.
2. Removes the unit from the hiddenUnits[] list.
"""
manSpy = """
spy(unit, unitType)
Game function

Causes a unit to search for hidden units. Information is then passed on to the player at the umpire's discretion.

1. Checks if the unitType has the ability to search. If not, the function throws an error and quits.
2. Randomly determines the search effectiveness between 1 and 6.
3. If the effectiveness is 6: tells the umpire to give good information, and calls details().
4. If the effectiveness is 1: tells the umpire to give wrong information, and calls details().
5. If the effectiveness is 2, 3, 4, or 5: tells the umpire to give no information.
6. Adds the unit to the usedUnits[] list.
"""
manTorpedo = """
torpedo(unit, unitType)
Game function

Causes a unit to fire a torpedo.

1. Checks if the unitType has the ability to fire torpedoes. If not, the function throws an erorr and quits.
2. Generates a torpedo effectiveness number between 1 and 6. If the number is six, manual(kill) is called. If the number is anything else, attack() is called.
3. Adds the unit to the usedUnits[] and immobileUnits[] lists.
"""

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
    if unitType in attack4: maximum = 4
    elif unitType in attack6: maximum = 6
    elif unitType in attack8: maximum = 8
    elif unitType in attack12: maximum = 12
    elif unitType in attack16: maximum = 16
    elif unitType in attack20: maximum = 20
    elif unitType in attack24: maximum = 24
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
    if unitType in attack4: maximum = 4
    elif unitType in attack12: maximum = 12
    elif unitType in attack20: maximum = 20
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
    if unitType in fire8: maximum = 4
    elif unitType in fire10: maximum = 10
    elif unitType in fire12: maximum = 12
    elif unitType in fire16: maximum = 16
    elif unitType in fire20: maximum = 20
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
    if unitType in build4: print("Fortification of strength", random.randrange(1,4), "built.")
    elif unitType in build8: print("Fortification of strength", random.randrange(1,8), "built.")
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
    searchEffectiveness = random.randrange(1,6)
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
    torpedoEffectiveness = random.randrange(1,6)
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

# def sortie(unit, unitType):
# def depthcharge(unit, unitType):

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
    # elif argument == "sortie": print(manSortie)
    # elif argument == "depthcharge": print(manDepthcharge)

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
    # elif command == "sortie": sortie(unit, unitType)
    # elif command == "depthcharge": missile(unit, unitType)
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

# Game loop
while warPhase == True:
    prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "]% "
    command = input(prompt)
    if command == "turn":
        usedUnits.clear()
        immobileUnits.clear()
        round = round + 1
    elif command == "quit": 
        score()
        warPhase = False
    elif command == "help":
        print("turn, quit, man, help, details, score, new")
        print(*validCommands, sep = ", ")
        print(*allUnitTypes, sep = ", ")
    elif command == "details": details()
    elif command == "score": score()
    elif command == "man":
        subPrompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + command + "]% "
        argument = input(subPrompt)
        man(argument)
    elif command == "manual":
        subPrompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + command + "]% "
        argument = input(subPrompt)
        manual(argument)
    elif command in validCommands:
        subPrompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + command + "]% "
        unit, unitType = input(subPrompt).split()
        getCommand(command, unit, unitType)
    else: print("Unknown command.")
    commandNumber = commandNumber + 1