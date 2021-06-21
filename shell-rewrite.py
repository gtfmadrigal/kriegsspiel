import random
from normandy import *

# Strings
round = 1
commandNumber = 1
secrets = ""
airPhase = True
campaign = "Normandy"
firstHealth = sum(firstTeamTable.values())
secondHealth = sum(secondTeamTable.values())
helpTextBlock = """
Umpire commands: score, turn, details, quit, help, health, kill, freeze, convert, disable, merge, split, info, use
Theater-agnostic commands: attack, move, hide, reveal, spy, fire
Naval commands: heading, torpedo, sortie, depthcharge, board
Army commands: build, missile
Air commands: takeoff, land, pulse, airlift, survey, bomb, kamikaze, dogfight
"""

# Lists
usedUnits = []
immobileUnits = []
hiddenUnits = []
alreadyDropped = []
defendingUnits = []
disabledUnits = []
deadUnits = []
firstTeamFlying = []
secondTeamFlying = []
ships = []
convertTable = ["light-artillery", "med-artillery", "heavy-artillery", "light-cavalry", "med-cavalry", "heavy-cavalry"]

# Dictionaries
errorMessages = {"argument":"Bad argument for command. Type 'man [command] for details.", "team":"That unit belongs to the wrong team.", "available":"That unit is currently unavailable.", "function":"That function is unavailable to this unit.", "heading":"Unit cannot exceed its maximum heading change.", "dead":"Unit is dead.", "type":"No such unit type.", "unit":"No such unit.", "hidden":"Unit is already hidden.", "required":"Heading changes are not required for this unit.", "airborne":"Unit is not airborne.", "board":"Unit is not a boardable ship", "exists":"A unit with that name already exists."}
dividedTable = {}
healthTable = {"infantry":4, "engineers":4, "mechanized":6, "light-artillery":8, "med-artillery":9, "heavy-artillery":10, "light-cavalry":12, "med-cavalry":14, "heavy-cavalry":16, "special":20, "corvette":4, "amphibious":4, "patrol":2, "cruiser":10, "destroyer":8, "battleship":12, "carrier":16, "attack-submarine":1, "missile-submarine":1, "light-fighter":4, "heavy-fighter":8, "bomber":12, "stealth-bomber":10, "recon":4, "transport":12, "drone":4}
movementTable = {"infantry":10, "engineers":10, "mechanized":15, "light-artillery":10, "med-artillery":7, "heavy-artillery":5, "light-cavalry":10, "med-cavalry":7, "heavy-cavalry":5, "special":15, "corvette":15, "amphibious":15, "patrol":15, "cruiser":7, "destroyer":10, "battleship":5, "carrier":5, "attack-submarine":15, "missile-submarine":15, "light-fighter":30, "heavy-fighter":15, "bomber":15, "stealth-bomber":10, "recon":20, "transport":30, "drone":30}
hideTable = {"infantry":1, "engineers":1, "mechanized":1, "light-artillery":1, "med-artillery":1, "heavy-artillery":1, "special":1, "attack-submarine":1, "missile-submarine":1, "stealth-bomber":1, "recon":1, "drone":1}
spyTable = {"infantry":6, "engineers":6, "mechanized":6, "recon":6, "drone":6}
attackTable = {"infantry":4, "engineers":4, "mechanized":4, "light-artillery":4, "med-artillery":4, "heavy-artillery":4, "light-cavalry":6, "med-cavalry":8, "heavy-cavalry":10, "special":20, "corvette":6, "amphibious":4, "patrol":4, "cruiser":16, "destroyer":8, "battleship":12, "carrier":12, "light-fighter":4, "heavy-fighter":6, "bomber":4, "stealth-bomber":4, "recon":4, "transport":4, "drone":4}
splitTable = {"infantry":4, "engineers":4, "mechanized":6, "light-artillery":8, "med-artillery":9, "heavy-artillery":10, "light-cavalry":12, "med-cavalry":14, "heavy-cavalry":16, "special":20}
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
bombTable = {"bomber":8, "stealth-bomber":6, "drone":10}
flyTable = {"light-fighter":1, "heavy-fighter":1, "bomber":1, "stealth-bomber":1, "recon":1, "transport":1, "drone":1}
manTable = {}
structureTable = {}

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

def error(code, function):
    print(errorMessages.get(code))
    print("Error message called by", str(function))

def remove(item, list):
    global usedUnits
    global immobileUnits
    global hiddenUnits
    global disabledUnits
    global alreadyDropped
    global defendingUnits
    global deadUnits
    global firstTeamFlying
    global secondTeamFlying
    list.remove(item)

def append(item, list):
    global usedUnits
    global immobileUnits
    global hiddenUnits
    global disabledUnits
    global alreadyDropped
    global defendingUnits
    global deadUnits
    global firstTeamFlying
    global secondTeamFlying
    list.append(item)

def clear(list):
    global usedUnits
    global immobileUnits
    global hiddenUnits
    global disabledUnits
    global alreadyDropped
    global defendingUnits
    global deadUnits
    global firstTeamFlying
    global secondTeamFlying
    list.clear()

def check(item, table):
    if item in table: return True
    elif not item in table: return False

def reduce(unit, unitType):
    export = 0
    if locationTable.get(unit) == "hill": 
        if unitType == "mechanized": pass
        elif unitType == "special": pass
        else: export = export + 1
    elif locationTable.get(unit) == "forest":
        if unitType == "infantry": pass
        elif unitType == "light-artillery": pass
        elif unitType == "med-artillery": pass
        elif unitType == "heavy-artillery": pass
        elif unitType == "special": pass
        else: export = export + 1
    elif locationTable.get(unit) == "swamp": export = export + 1
    elif locationTable.get(unit) in structureTable: export = structureTable.get(locationTable.get(unit))

def fortificationReduce(structure, damage):
    global structureTable
    initialNetDamage = structureTable.get(structure) - damage
    if initialNetDamage > 0:
        structureTable[structure] = initialNetDamage
        print(structure, "new value:", str(initialNetDamage))
        return 0
    else:
        print(structure, "destroyed.")
        del structureTable[structure]
        finalNetDamage = abs(initialNetDamage)
        return finalNetDamage

def damage(unit, unitType, table):
    if check(unit, immobileUnits) == True or check(unit, usedUnits) == True:
        error("available", "damage")
        return
    if check(unit, deadUnits) == True:
        error("dead", "damage")
        return
    if check(unit, table) == False: return
    basicMaximum = float(table.get(unitType)) + 1
    multiplier = dividedTable.get(unit, 1)
    maximum = basicMaximum * multiplier
    return random.randrange(1, maximum)

def fog():
    if fogOfWar == 1: return False
    export = random.randrange(1, fogOfWar + 1)
    if export == 1: return True
    else: return False

# Umpire commands
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
    clear(usedUnits)
    clear(immobileUnits)
    clear(alreadyDropped)
    for x in disabledUnits: freeze(x)
    clear(disabledUnits)
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
    print(*allUnitTypes.keys(), sep = ", ")

def kill(arguments):
    global firstTeamTable
    global secondTeamTable
    unit = arguments[2]
    if unit in firstTeamTable: table = firstTeamTable
    elif unit in secondTeamTable: table = secondTeamTable
    else: 
        error("unit", "kill")
        return
    del table[unit]
    append(unit, deadUnits)
    update()

def health(arguments):
    global firstTeamTable
    global secondTeamTable
    unit = arguments[2]
    newHealth = float(arguments[3])
    if unit in firstTeamTable: table = firstTeamTable
    elif unit in secondTeamTable: table = secondTeamTable
    else:
        error("unit", "health")
        return
    currentHealth = table.get(unit)
    if newHealth <= 0: kill(arguments)
    else: table[unit] = float(newHealth)
    update()

def freeze(arguments):
    unit = arguments[2]
    append(unit, immobileUnits)

def convert(arguments, teamTable):
    global firstTeamTable
    global secondTeamTable
    global unitTable
    unit = arguments[2]
    if not unit in teamTable:
        error("team", "convert")
        return
    if not unit in convertTable:
        error("function", "convert")
        return
    currentHealth = teamTable.get(unit)
    unitTable[unit] = "infantry"
    if currentHealth > 4: newHealth = 4
    else: newHealth = currentHealth
    teamTable[unit] = newHealth
    update()

def disable(arguments):
    unit = arguments[2]
    freeze(unit)
    use(unit)
    append(unit, disabledUnits)

def merge():
    pass

def split():
    pass

def info():
    pass

def use():
    pass

def man():
    pass

# Theater-agnostic functions
def attack():
    pass

def move():
    pass

def hide():
    pass

def reveal():
    pass

def spy():
    pass

def fire():
    pass

# Naval functions
def heading():
    pass

def torpedo():
    pass

def sortie():
    pass

def depthcharge():
    pass

def board():
    pass

# Army functions
def build():
    pass

def missile():
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

def kamikaze():
    pass

# Shell functions
def info():
    pass

def airShell(team, targetTeam, teamTable, targetTeamTable, teamFlyingTable, targetTeamFlyingTable):
    pass

def shell(team, targetTeam, teamTable, targetTeamTable, teamFlyingTable, targetTeamFlyingTable):
    global airPhase
    global commandNumber
    #if airPhase == True and airTheater == True:
        #airShell(team, targetTeam, teamTable, targetTeamTable, teamFlyingTable, targetTeamFlyingTable)
        #return
    prompt = str(round) + " ~ " + str(commandNumber) + " " + str(campaign) + ":" + str(team) + " % "
    rawCommand = input(prompt)
    parsedCommand = rawCommand.split()
    commandFog = fog()
    if commandFog == True:
        print("This command fails.")
        commandNumber = commandNumber + 1
        return
    if parsedCommand[1] == "score": score()
    elif parsedCommand[1] == "turn": turn()
    elif parsedCommand[1] == "details": details()
    elif parsedCommand[1] == "quit": quitGame()
    elif parsedCommand[1] == "help": helpText()
    elif parsedCommand[1] == "health": health(parsedCommand)
    elif parsedCommand[1] == "kill": kill(parsedCommand)
    elif parsedCommand[1] == "man": man(parsedCommand)
    elif parsedCommand[1] == "freeze": freeze(parsedCommand)
    elif parsedCommand[1] == "convert": pass
    elif parsedCommand[1] == "disable": pass
    elif parsedCommand[1] == "merge": pass
    elif parsedCommand[1] == "split": pass
    elif parsedCommand[1] == "info": pass
    elif parsedCommand[1] == "use": pass
    elif parsedCommand[1] == "attack": pass
    elif parsedCommand[1] == "move": pass
    elif parsedCommand[1] == "hide": pass
    elif parsedCommand[1] == "reveal": pass
    elif parsedCommand[1] == "spy": pass
    elif parsedCommand[1] == "fire": pass
    elif parsedCommand[1] == "heading": pass
    elif parsedCommand[1] == "torpedo": pass
    elif parsedCommand[1] == "sortie": pass
    elif parsedCommand[1] == "depthcharge": pass
    elif parsedCommand[1] == "board": pass
    elif parsedCommand[1] == "build": pass
    elif parsedCommand[1] == "missile": pass
    else:
        print("Unknown command. Type 'help' to see a list of commands, or 'man [command]' to see how to use a particular command.")
        return
    commandNumber = commandNumber + 1

while True:
    while (round % 2) != 0: shell(firstTeam, secondTeam, firstTeamTable, secondTeamTable, firstTeamFlying, secondTeamFlying)
    while (round % 2) == 0: shell(secondTeam, firstTeam, secondTeamTable, firstTeamTable, secondTeamFlying, firstTeamFlying)