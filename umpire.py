# Definitions
import random
from normandy import *

round = 1
commandNumber = 1
secrets = ""
airPhase = True
firstHealth = sum(firstTeamTable.values())
secondHealth = sum(secondTeamTable.values())
helpTextBlock = """
Umpire commands: score, turn, details, quit, help, health, kill, freeze, convert, disable, merge, split, info, use
Theater-agnostic commands: attack, move, hide, reveal, spy, fire
Naval commands: heading, torpedo, sortie, depthcharge, board
Army commands: build, missile
Air commands: takeoff, land, pulse, airlift, survey, bomb, kamikaze, dogfight
"""

usedUnits = []
immobileUnits = []
hiddenUnits = []
alreadyDropped = []
defendingUnits = []
disabledUnits = []
deadUnits = []
agnosticCommands = ["move", "hide", "reveal", "spy", "fire", "convert"]
navyCommands = ["heading", "torpedo", "sortie", "depthcharge", "board"]
armyCommands = ["build", "missile", "convert"]
airCommands = ["takeoff", "land", "pulse", "airlift", "survey", "bomb", "kamikaze", "dogfight"]
umpireCommands = ["score", "turn", "details", "quit", "help", "health", "kill", "freeze", "disable", "merge", "split", "info", "use"]
firstTeamFlying = []
secondTeamFlying = []
ships = []

errorMessages = {"arguments":"Too many arguments for command. Type 'man' [command] for information.", "os":"Unknown operating system.", "bad":"Bad command. Type 'help' for assistance.", "team":"That unit belongs to the wrong team.", "available":"That unit is currently unavailable.", "function":"That function is unavailable to this unit.", "heading":"Unit cannot exceed its maximum heading change.", "dead":"Unit is dead.", "type":"No such unit type.", "unit":"No such unit.", "hidden":"Unit is already hidden.", "required":"Heading changes are not required for this unit.", "airborne":"Unit is not airborne.", "board":"Unit is not a boardable ship"}
dividedTable = {}
healthTable = {"infantry":4, "engineers":4, "mechanized":6, "light-artillery":8, "med-artillery":9, "heavy-artillery":10, "light-cavalry":12, "med-cavalry":14, "heavy-cavalry":16, "special":20, "corvette":4, "amphibious":4, "patrol":2, "cruiser":10, "destroyer":8, "battleship":12, "carrier":16, "attack-submarine":1, "missile-submarine":1, "light-fighter":4, "heavy-fighter":8, "bomber":12, "stealth-bomber":10, "recon":4, "transport":12, "drone":4}
movementTable = {"infantry":10, "engineers":10, "mechanized":15, "light-artillery":10, "med-artillery":7, "heavy-artillery":5, "light-cavalry":10, "med-cavalry":7, "heavy-cavalry":5, "special":15, "corvette":15, "amphibious":15, "patrol":15, "cruiser":7, "destroyer":10, "battleship":5, "carrier":5, "attack-submarine":15, "missile-submarine":15, "light-fighter":30, "heavy-fighter":15, "bomber":15, "stealth-bomber":10, "recon":20, "transport":30, "drone":30}
hideTable = {"infantry":1, "engineers":1, "mechanized":1, "light-artillery":1, "med-artillery":1, "heavy-artillery":1, "special":1, "attack-submarine":1, "missile-submarine":1, "stealth-bomber":1, "recon":1, "drone":1}
spyTable = {"infantry":6, "engineers":6, "mechanized":6, "recon":6, "drone":6}
attackTable = {"infantry":4, "engineers":4, "mechanized":4, "light-artillery":4, "med-artillery":4, "heavy-artillery":4, "light-cavalry":6, "med-cavalry":8, "heavy-cavalry":10, "special":20, "corvette":6, "amphibious":4, "patrol":4, "cruiser":16, "destroyer":8, "battleship":12, "carrier":12, "light-fighter":4, "heavy-fighter":6, "bomber":4, "stealth-bomber":4, "recon":4, "transport":4, "drone":4}
splitTable = {"infantry":4, "engineers":4, "mechanized":6, "light-artillery":8, "med-artillery":9, "heavy-artillery":10, "light-cavalry":12, "med-cavalry":14, "heavy-cavalry":16, "special":20}
convertTable = {"light-artillery":1, "med-artillery":1, "heavy-artillery":1, "light-cavalry":1, "med-cavalry":1, "heavy-cavalry":1}
fireTable = {"light-artillery":8, "med-artillery":9, "heavy-artillery":10, "light-cavalry":12, "med-cavalry":16, "heavy-cavalry":20, "corvette":6, "cruiser":20, "destroyer":10, "battleship":16, "bomber":8, "stealth-bomber":6, "drone":4}
headingTable = {"corvette":1, "cruiser":1, "destroyer":1, "battleship":1, "carrier":1}
torpedoTable = {"attack-submarine":6, "missile-submarine":6}
sortieTable = {"carrier":8}
sortieDefenseTable = {"corvette":12, "amphibious":4, "cruiser":12, "destroyer":12, "battleship":6, "carrier":8}
depthchargeTable = {"corvette":6, "amphibious":6, "cruiser":6, "destroyer":6, "battleship":6, "carrier":6}
boardTable = {"corvette":6, "amphibious":6, "patrol":6, "cruiser":8, "destroyer":10, "carrier":6}
buildTable = {"infantry":4, "engineers":8, "mechanized":4, "special":6}
missileTable = {"destroyer":8, "missile-submarine":16, "light-fighter":6, "heavy-fighter":6, "bomber":8, "stealth-bomber":8}
pulseTable = {"bomber":6, "stealth-bomber":6}
transportTable = {"transport":1}
kamikazeTable = {"light-fighter":6, "heavy-fighter":8}
moveFireTable = {"infantry":1, "engineers":1, "mechanized":1, "light-cavalry":1, "med-cavalry":1, "heavy-cavalry":1, "special":1, "corvette":1, "amphibious":1, "patrol":1, "cruiser":1, "destroyer":1, "battleship":1, "carrier":1, "light-fighter":1, "heavy-fighter":1, "bomber":1, "stealth-bomber":1, "recon":4, "transport":1, "drone":1}
bombTable = {}
flyTable = {}

# Initialization work
loadGame()

# Meta-functions
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
    global disabledUnits
    global alreadyDropped
    global defendingUnits
    global deadUnits
    global firstTeamFlying
    global secondTeamFlying
    if command == "append": list.append(unit)
    elif command == "clear": list.clear()
    elif command == "remove": list.remove(unit)

def evaluate(unit, unitType, table):
    if unit in immobileUnits or unit in usedUnits:
        print(errorMessages.get("available"))
        return
    if unit in deadUnits:
        print(errorMessages.get("dead"))
        return
    basicMaximum = table.get(unitType) + 1
    modifier = modification(unit)
    maximum = basicMaximum * modifier
    return random.randrange(1, maximum)

def prompt(team, airShell, function, level):
    if level == "player": promptChar = "% "
    elif level == "umpire": promptChar = "# "
    if function == None: intermediate = " "
    else: intermediate = " " + str(function) + " "
    if airShell == True: shellPrompt = str(round) + " ~ " + str(commandNumber) + " " + str(team) + "-air" + intermediate + promptChar
    else: shellPrompt = str(round) + " ~ " + str(commandNumber) + " " + str(team) + intermediate + promptChar
    command = input(shellPrompt)
    return command

def modification(unit):
    if dividedTable.get(unit) == None: return 1
    else: return dividedTable.get(unit)

def fog():
    if fogOfWar == 1: return False
    returnable = random.randrange(1, fogOfWar + 1)
    if returnable == 1: return True
    return False

# One-word command functions
def score():
    update()
    firstPercent = firstHealth / firstHealthTotal * 100
    secondPercent = secondHealth / secondHealthTotal * 100
    print(firstTeam, "total health:", firstHealth, "or", firstPercent, "%")
    print(secondTeam, "total health:", secondHealth, "or", secondPercent, "%")

def turn():
    global round
    global airPhase
    score()
    changeList(True, usedUnits, "clear")
    changeList(True, immobileUnits, "clear")
    changeList(True, alreadyDropped, "clear")
    for x in disabledUnits: freeze(x)
    changeList(True, disabledUnits, "clear")
    round = round + 1
    airPhase = True

def details():
    print("Secrets:")
    print(secrets)
    print("Hidden units:")
    print(*hiddenUnits, sep = ", ")
    score()

def quitGame():
    areYouSure = input("Are you sure you want to quit? [Yes/no]: ")
    if areYouSure == "yes" or areYouSure == "y":
        score()
        quit()

def helpText():
    print("Commands: ")
    print(helpTextBlock)
    print("Unit types:")
    print(*allUnitTypes, sep = ", ")

def attack(team, targetTeam, targetTeamTable):
    global firstTeamTable
    global secondTeamTable
    attackPhase = True
    defensePhase = False
    willQuit = False
    totalAttackDamage = 0
    totalDefenseDamage = 0
    while attackPhase == True:
        command = prompt(team, False, "attack", "player")
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
            attackDamage = evaluate(command, unitType, attackTable)
            if attackDamage == None: continue
            if command in hiddenUnits: reveal(command, unitType)
            totalAttackDamage = totalAttackDamage + attackDamage
            use(command)
            if not command in moveFireTable: freeze(command)
            print("Damage dealt:", attackDamage)
            print("Total damage dealt:", totalAttackDamage)
        else: print(errorMessages.get("bad"))
    while defensePhase == True:
        command = prompt(targetTeam, False, "defend", "player")
        if command == "help": print("Enter a named unit to defend, 'save' to save changes to gamestate, or 'quit' to exit without saving.")
        elif command == "quit":
            defensePhase = False
            willQuit = True
        elif command == "save": defensePhase = False
        elif command in unitTable:
            unitType = unitTable.get(command)
            defenseDamage = evaluate(command, unitType, attackTable)
            if defenseDamage == None: continue
            if command in hiddenUnits: reveal(command, unitType)
            totalDefenseDamage = totalDefenseDamage + defenseDamage
            changeList(command, defendingUnits, "append")
            print("Defense dealt:", defenseDamage)
            print("Total defense dealt:", totalDefenseDamage)
            if totalDefenseDamage >= totalAttackDamage: defensePhase = False
        else: print(errorMessages.get("bad"))
    if willQuit == True: return
    if totalDefenseDamage >= totalAttackDamage: print("Attack repelled by", targetTeam)
    else:
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
    turn()

# Umpire functions
def health(unit):
    global firstTeamTable
    global secondTeamTable
    if unit in firstTeamTable: 
        relevantTeam = firstTeam
        relevantTable = firstTeamTable
    elif unit in secondTeamTable:
        relevantTeam = secondTeam
        relevantTable = secondTeamTable
    else:
        print(errorMessages.get("unit"))
        return
    print("Current health: ", relevantTable.get(unit))
    newHealth = prompt(relevantTeam, False, "health", "umpire")
    if int(newHealth) <= 0: kill(unit, relevantTable)
    else: relevantTable[unit] = float(newHealth)
    update()

def kill(unit, teamTable):
    global firstTeamTable
    global secondTeamTable
    del teamTable[unit]
    changeList(unit, deadUnits, "append")
    update()

def freeze(unit):
    changeList(unit, immobileUnits, "append")

def disable(unit):
    freeze(unit)
    changeList(unit, disabledUnits, "append")

def use(unit):
    changeList(unit, usedUnits, "append")

def merge(team, teamTable):
    global firstTeamTable
    global secondTeamTable
    global unitTable
    global dividedTable
    mergePhase = True
    willQuit = False
    unitType = input("New unit type: ")
    if not unitType in allUnitTypes:
        print("No such unit type.")
        return
    unitHealth = 0
    mergedUnits = []
    usedTrue = False
    immobileTrue = False
    disabledTrue = False
    numberOfUnits = 0
    while mergePhase == True:
        command = prompt(team, False, "merge", "player")
        if command == "save": mergePhase = False
        elif command == "quit":
            mergePhase = False
            willQuit = True
        elif command in teamTable:
            commandUnitType = unitTable.get(command)
            if commandUnitType == unitType: 
                mergedUnits.append(command)
                if command in usedUnits: usedTrue = True
                if command in immobileUnits: immobileTrue = True
                if command in disabledUnits: disabledTrue = True
                unitHealth = unitHealth + teamTable.get(command)
                del teamTable[command]
                numberOfUnits = numberOfUnits + 1
            else: print("Wrong unit type.")
        else: print(errorMessages.get("unit"))
    if willQuit == True: return
    newUnit = prompt(team, False, "unified", "umpire")
    unitTable[newUnit] = unitType
    teamTable[newUnit] = unitHealth
    dividedTable[newUnit] = numberOfUnits
    for x in mergedUnits: del teamTable[x]
    if usedTrue == True: use(newUnit)
    if immobileUnits == True: freeze(newUnit)
    if disabledUnits == True: disable(newUnit)

def split(unit, unitType, team, teamTable):
    global firstTeamTable
    global secondTeamTable
    global dividedTable
    global unitTable
    if not unit in dividedTable or not unitType in splitTable:
        print(errorMessages.get("function"))
        return
    splitPhase = True
    willQuit = False
    numberOfUnits = 0
    newUnits = []
    currentHealth = teamTable.get(unit)
    while splitPhase == True:
        command = prompt(team, False, "split", "umpire")
        if command == "save": splitPhase = False
        elif command == "quit":
            splitPhase = False
            willQuit = True
        elif command in unitTable: print("Unit already exists.")
        elif len(command.split()) == 1:
            numberOfUnits = numberOfUnits + 1
            newUnits.append(command)
        else: print(errorMessages.get("command"))
    if willQuit == True: return
    newHealth = currentHealth / numberOfUnits
    del teamTable[unit]
    del unitTable[unit]
    if unit in dividedTable: del dividedTable[unit]
    for x in newUnits:
        teamTable[x] = newHealth
        unitTable[x] = unitType

# Theater-agnostic functions
def move(unit, unitType):
    if unit in immobileUnits:
        print(errorMessages.get("function"))
        return
    if unitType in headingTable: print(errorMessages.get("heading"))
    if not unitType in moveFireTable: use(unit)
    freeze(unit)

def hide(unit, unitType, team):
    global secrets
    if not unitType in hideTable:
        print(errorMessages.get("function"))
        return
    if unit in hiddenUnits:
        print(errorMessages.get("hidden"))
        return
    location = prompt(team, False, "hide", "player")
    newSecret = unit + " " + location
    secrets = secrets + ", " + newSecret
    changeList(unit, hiddenUnits, "append")

def reveal(unit, unitType):
    global secrets
    if not unit in hiddenUnits or not unitType in hideTable:
        print(errorMessages.get("function"))
        return
    changeList(unit, hiddenUnits, "remove")
    append = unit + "is no longer hidden."
    secrets = secrets + append

def spy(unit, unitType):
    if not unitType in spyTable:
        print(errorMessages.get("function"))
        return
    effectiveness = evaluate(unit, unitType, spyTable)
    if effectiveness == 6: print("Good information.")
    elif effectiveness == 1: print("Bad information.")
    elif effectiveness == None: return
    else: print("No information.")
    details()
    use(unit)

def fire(unit, unitType, team, targetTeamTable, version, table):
    global firstTeamTable
    global secondTeamTable
    defensePhase = True
    willQuit = False
    if not unitType in table:
        print(errorMessages.get("function"))
        return
    if unit in hiddenUnits: reveal(unit, unitType)
    while defensePhase == True:
        command = prompt(team, False, version, "player")
        if command == "help": print("Enter a named unit, 'save' to save changes to gamestate, or 'quit' to exit without saving.")
        elif command == "quit":
            defensePhase = False
            willQuit = True
        elif command == "save": defensePhase = False
        elif command in unitTable:
            try: changeList(command, defendingUnits, "append")
            except: pass
        else: print(errorMessages.get("bad"))
    if willQuit == True: return
    damage = evaluate(unit, unitType, table)
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
    changeList(True, defendingUnits, "clear")
    score()

# Naval functions
def heading(unit, unitType):
    if evaluate(unit, unitType, headingTable) == 1:
        freeze(unit)
        if not unitType in moveFireTable: use(unit)
    else:
        print(errorMessages.get("required"))
        return

def torpedo(unit, unitType, team, targetTeamTable):
    global firstTeamTable
    global secondTeamTable
    if not unitType in torpedoTable:
        print(errorMessages.get("function"))
        return
    damage = evaluate(unit, unitType, torpedoTable)
    target = prompt(team, False, "torpedo", "player")
    if not target in targetTeamTable:
        print(errorMessages.get("team"))
    oldHealth = targetTeamTable.get(target)
    if damage == 6 or oldHealth - damage <= 0:
        print(target, "sunk.")
        kill(target, targetTeamTable)
    else:
        newHealth = oldHealth - damage
        print(target, "new health:", newHealth)
        targetTeamTable[target] = newHealth
    use(unit)
    freeze(unit)
    score()

def sortie(unit, unitType, team, targetTeamTable):
    global firstTeamTable
    global secondTeamTable
    if not unitType in sortieTable:
        print(errorMessages.get("function"))
        return
    attackDamage = evaluate(unit, unitType, sortieTable)
    if attackDamage == None:
        print(errorMessages.get("function"))
        return
    target = prompt(team, False, "sortie", "player")
    if not target in targetTeamTable:
        print(errorMessages.get("team"))
        return
    targetUnitType = unitTable.get(target)
    defenseDamage = evaluate(target, targetUnitType, sortieDefenseTable)
    if defenseDamage == None: defenseDamage = 0
    if defenseDamage <= attackDamage:
        netDamage = attackDamage - defenseDamage
        oldHealth = targetTeamTable[target]
        if oldHealth - netDamage < 0: kill(target, targetTeamTable)
        else: 
            newHealth = oldHealth - netDamage
            print(target, "new health:", newHealth)
            targetTeamTable[target] = newHealth
    else: print("Attack repelled by:", target)
    use(unit)
    freeze(unit)
    score()

def depthcharge(unit, unitType, team, targetTeamTable):
    if not unitType in depthchargeTable:
        print(errorMessages.get("function"))
        return
    if unit in alreadyDropped:
        print(errorMessages.get("available"))
        return
    target = prompt(team, False, "depthcharge", "player")
    effectiveness = evaluate(unit, unitType, depthchargeTable)
    if effectiveness == 6: 
        kill(target, targetTeamTable)
        print(target, "sunk.")
    elif effectiveness == 5:
        changeList(target, immobileUnits, "append")
        changeList(target, disabledUnits, "append")
        print(target, "frozen.")
    elif effectiveness == None: return
    else: print("Missed.")
    freeze(unit)
    changeList(unit, alreadyDropped, "append")
    score()

def board(unit, unitType, team, teamTable, targetTeamTable):
    global firstTeamTable
    global secondTeamTable
    if not unitType in boardTable:
        print(errorMessages.get("function"))
        return
    target = prompt(team, False, "board", "player")
    if not target in targetTeamTable:
        print(errorMessages.get("unit"))
        return
    targetUnitType = unitTable.get(target)
    if not targetUnitType in ships:
        print("board")
        return
    effectiveness = evaluate(unit, unitType, boardTable)
    currentHealth = teamTable.get(unit)
    if effectiveness >= 5:
        print(target, "seized.")
        targetHealth = targetTeamTable.get(target)
        del targetTeamTable[target]
        teamTable[target] = targetHealth
    else:
        print("Boarding attempt failed.")
        print(unit, "suffers", str(effectiveness), "damage.")
        newHealth = currentHealth - effectiveness
        if newHealth <= 0:
            kill(unit, teamTable)
            kill(unit, "sunk.")
        else: 
            teamTable[unit] = newHealth
    freeze(unit)
    changeList(unit, alreadyDropped, "append")
    update()

# Army functions
def build(unit, unitType):
    if not unitType in buildTable:
        print(errorMessages.get("function"))
        return
    fortification = evaluate(unit, unitType, buildTable)
    print("Fortification of strength", fortification, "built.")
    use(unit)
    freeze(unit)

def missile(unit, unitType, team, targetTeamTable):
    global firstTeamTable
    global secondTeamTable
    if not unitType in missileTable:
        print(errorMessages.get("function"))
        return
    if unit in hiddenUnits: reveal(unit, unitType)
    attackDamage = evaluate(unit, unitType, missileTable)
    if attackDamage == None: return
    command = prompt(team, False, "missile", "player")
    if command not in targetTeamTable:
        print(errorMessages.get("team"))
        return
    targetUnitType = unitTable.get(command)
    defenseDamage = evaluate(command, targetUnitType, missileTable)
    if defenseDamage == None: netDamage = attackDamage
    else: netDamage = attackDamage - defenseDamage
    currentHealth = targetTeamTable.get(command)
    if netDamage >= currentHealth: kill(command, targetTeamTable)
    elif netDamage >= 0:
        print("Missile repelled.")
        return
    else:
        newHealth = currentHealth - netDamage
        targetTeamTable[command] = newHealth
    use(unit)
    if not unit in moveFireTable: freeze(unit)
    score()

def convert(unit, unitType, teamTable):
    global firstTeamTable
    global secondTeamTable
    global unitTable
    if not unitType in convertTable:
        print(errorMessages.get("function"))
        return
    currentHealth = teamTable.get(unit)
    unitTable[unit] = "infantry"
    if currentHealth > 4: newHealth = 4
    else: newHealth = currentHealth
    teamTable[unit] = newHealth

# Air functions
def takeoff(unit, teamFlyingTable):
    if unit in teamFlyingTable:
        print("Already airborne.")
        return
    changeList(unit, teamFlyingTable, "append")

def land(unit, teamFlyingTable):
    changeList(unit, teamFlyingTable, "remove")
    use(unit)

def pulse(unit, unitType, team, targetTeamTable):
    effectiveness = evaluate(unit, unitType, pulseTable)
    if effectiveness == 6:
        print("Pulse effective.")
        pulsePhase = True
        pulsedUnits = []
    elif effectiveness == None: 
        print(errorMessages.get("function"))
        return
    else: 
        print("Pulse ineffective.")
        return
    while pulsePhase == True:
        command = prompt(team, False, "pulse", "player")
        if command in targetTeamTable: pulsedUnits.append(command)
        elif command == "help": print("Enter a unit that has been disabled, 'quit' to exit, or 'save' to exit and save.")
        elif command == "quit": return
        elif command == "save": 
            for x in pulsedUnits: disable(x)
            return
        else: print(errorMessages.get("unit"))
    use(unit)

def airlift(unit, unitType, team, teamTable):
    if not unitType in transportTable:
        print(errorMessages.get("function"))
        return
    liftedUnit = prompt(team, False, "airlift", "player")
    if not liftedUnit in teamTable:
        print(errorMessages.get("team"))
        return
    use(unit)

def kamikaze(unit, unitType, team, teamTable, targetTeamTable):
    global firstTeamTable
    global secondTeamTable
    if not unitType in kamikazeTable:
        print(errorMessages.get("function"))
        return
    target = prompt(team, False, "kamikaze", "player")
    if not target in targetTeamTable:
        print(errorMessages.get("team"))
        return
    effectiveness = evaluate(unit, unitType, kamikazeTable)
    oldHealth = targetTeamTable.get(target)
    if effectiveness == 6 or oldHealth - effectiveness <= 0:
        print(target, "killed.")
        kill(target, targetTeamTable)
    else:
        newHealth = oldHealth - effectiveness
        print(target, "new health:", newHealth)
        targetTeamTable[target] = newHealth
    kill(unit, teamTable)

# Shell
def info(unit, unitType):
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
    if unitType in moveFireTable: print("Can move and fire in the same turn.")
    if unitType in torpedoTable: print("Can fire torpedoes.")
    if unitType in headingTable: print("Heading change required.")
    if unit in immobileUnits: print("Immovable this turn.")
    if unit in usedUnits: print("Unusable this turn.")
    if unit in hiddenUnits: print("Hidden.")

def umpireShell(command, unit):
    if command == "health": health(unit)
    elif command == "kill":
        if unit in firstTeamTable: teamTable = firstTeamTable
        else: teamTable = secondTeamTable
        kill(unit, teamTable)
    elif command == "freeze": freeze(unit)
    elif command == "disable": disable()
    elif command == "merge": merge()
    elif command == "use": use(unit)
    elif command == "split": split()

def airShell(team, targetTeam, teamTable, targetTeamTable, teamFlyingTable, targetTeamFlyingTable):
    global commandNumber
    global airPhase
    rawCommand = prompt(team, True, None, "player")
    if len(rawCommand.split()) == 2:
        command, unit = rawCommand.split()
        unitType = unitTable.get(unit)
        if not unit in unitTable:
            print(errorMessages.get("unit"))
            return
        if unit in deadUnits and not command == "health":
            print(errorMessages.get("dead"))
            return
        if not unitType in flyTable:
            print(errorMessages.get("function"))
            return
        if command in umpireCommands: umpireShell(command, unit)
        elif command in airCommands:
            if not unit in teamTable:
                print(errorMessages.get("team"))
                return
            if unit in deadUnits:
                print(errorMessages.get("dead"))
                return
            if unit in usedUnits:
                print(errorMessages.get("available"))
                return
            if not unit in teamFlyingTable and not command == "takeoff":
                print(errorMessages.get("airborne"))
                return
            if command == "takeoff": takeoff(unit, teamFlyingTable)
            elif command == "land": land(unit, teamFlyingTable)
            elif command == "pulse": pulse(unit, unitType, team, targetTeamTable)
            elif command == "airlift": airlift(unit, unitType, team, teamTable)
            elif command == "survey":spy(unit, unitType)
            elif command == "bomb": fire(unit, unitType, team, targetTeamTable, "bomb", bombTable)
            elif command == "missile": missile(unit, unitType, team, targetTeamTable)
            elif command == "kamikaze": kamikaze(unit, unitType, team, teamTable, targetTeamTable)
            elif command == "split": pass
        else: print(errorMessages.get("bad"))
    elif len(rawCommand.split()) == 1:
        if rawCommand == "dogfight": pass
        elif rawCommand == "next":
            changeList(True, usedUnits, "clear")
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
    airShell(team, targetTeam, teamTable, targetTeamTable, teamFlyingTable, targetTeamFlyingTable)

def shell(team, targetTeam, teamTable, targetTeamTable, teamFlyingTable, targetTeamFlyingTable):
    global airPhase
    global commandNumber
    if airPhase == True and airTheater == True: 
        airShell(team, targetTeam, teamTable, targetTeamTable, teamFlyingTable, targetTeamFlyingTable)
        return
    rawCommand = prompt(team, False, None, "player")
    commandFog = fog()
    if commandFog == True:
        print("This command fails.")
        return
    if len(rawCommand.split()) == 2:
        command, unit = rawCommand.split()
        if not unit in unitTable:
            print(errorMessages.get("unit"))
            return
        unitType = unitTable.get(unit)
        if command in umpireCommands: umpireShell(command, unit)
        elif command in navyCommands or command in armyCommands or command in agnosticCommands:
            if not unit in teamTable:
                print(errorMessages.get("team"))
                return
            if unit in deadUnits:
                print(errorMessages.get("dead"))
                return
            if unit in usedUnits:
                print(errorMessages.get("available"))
                return
            if command == "heading": heading(unit, unitType)
            elif command == "torpedo": torpedo(unit, unitType, team, targetTeamTable)
            elif command == "sortie": sortie(unit, unitType, team, targetTeamTable)
            elif command == "depthcharge": depthcharge(unit, unitType, team, targetTeamTable)
            elif command == "build": build(unit, unitType)
            elif command == "missile": missile(unit, unitType, team, targetTeamTable)
            elif command == "move": move(unit, unitType)
            elif command == "hide": hide(unit, unitType, team)
            elif command == "convert": convert(unit, unitType, teamTable)
            elif command == "info": info(unit, unitType)
            elif command == "reveal": reveal(unit, unitType)
            elif command == "spy": spy(unit, unitType)
            elif command == "fire": fire(unit, unitType, team, targetTeamTable, "fire", fireTable)
            elif command == "board": board(unit, unitType, team, teamTable, targetTeamTable)
            else:
                print(errorMessages.get("bad"))
                return
    elif len(rawCommand.split()) == 1:
        if rawCommand == "attack": attack(team, targetTeam, targetTeamTable)
        elif rawCommand == "score": score()
        elif rawCommand == "turn": turn()
        elif rawCommand == "quit": quitGame()
        elif rawCommand == "help": helpText()
        elif rawCommand == "merge": merge(team, teamTable)
        elif rawCommand == "details": details()
        else: print(errorMessages.get("bad"))
    else: 
        print(errorMessages.get("bad"))
        return
    commandNumber = commandNumber + 1

while True:
    while (round % 2) != 0: shell(firstTeam, secondTeam, firstTeamTable, secondTeamTable, firstTeamFlying, secondTeamFlying)
    while (round % 2) == 0: shell(secondTeam, firstTeam, secondTeamTable, firstTeamTable, secondTeamFlying, firstTeamFlying)