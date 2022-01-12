import random
import sys

# Strings
round = 1
commandNumber = 1
secrets = ""
airPhase = True
helpTextBlock = """
Umpire commands: score, turn, details, quit, help, health, kill, freeze, convert, disable, merge, split, info, use, man
Theater-agnostic commands: attack, move, hide, reveal, spy, fire
Naval commands: heading, torpedo, sortie, depthcharge, board
Army commands: build, missile
Air commands: takeoff, land, pulse, airlift, survey, bomb, kamikaze, dogfight, missile
"""

# List of lists
usedUnits = []
immobileUnits = []
hiddenUnits = []
alreadyDropped = []
defendingUnits = []
disabledUnits = []
deadUnits = []
firstTeamFlying = []
secondTeamFlying = []
convertTable = ["light-artillery", "med-artillery", "heavy-artillery", "light-cavalry", "med-cavalry", "heavy-cavalry"]
hideTable = ["infantry", "engineers", "mechanized", "light-artillery", "med-artillery", "heavy-artillery", "special", "attack-submarine", "missile-submarine", "stealth-bomber", "recon", "drone"]
hideableTerrain = ["forest", "swamp", "ocean", "air"]
airliftTable = ["infantry", "mechanized", "special", "light-cavalry"]

# Dictionaries
errorMessages = {"argument":"Bad argument for command. Type 'man [command]' for details.", "team":"That unit belongs to the wrong team.", "available":"That unit is currently unavailable.", "function":"That function is unavailable to this unit.", "heading":"Unit cannot change heading more than 45 degrees without calling the heading command.", "dead":"Unit is dead.", "type":"No such unit type.", "unit":"No such unit.", "hidden":"Unit is already hidden.", "required":"Heading changes are not required for this unit.", "airborne":"Unit is not airborne.", "board":"Unit is not a boardable ship", "exists":"A unit with that name already exists.", "terrain":"The terrain does not allow for that function to be called.", "command":"Unknown command. Type 'help' to see a list of commands, or 'man [command]' to see how to use a particular command.", "type":"Wrong datatype passed to command."}
dividedTable = {}
healthTable = {"infantry":4, "engineers":4, "mechanized":6, "light-artillery":8, "med-artillery":9, "heavy-artillery":10, "light-cavalry":12, "med-cavalry":14, "heavy-cavalry":16, "special":20, "corvette":4, "amphibious":4, "patrol":2, "cruiser":10, "destroyer":8, "battleship":12, "carrier":16, "attack-submarine":1, "missile-submarine":1, "light-fighter":4, "heavy-fighter":8, "bomber":12, "stealth-bomber":10, "recon":4, "transport":12, "drone":4}
movementTable = {"infantry":10, "engineers":10, "mechanized":15, "light-artillery":10, "med-artillery":7, "heavy-artillery":5, "light-cavalry":10, "med-cavalry":7, "heavy-cavalry":5, "special":15, "corvette":15, "amphibious":15, "patrol":15, "cruiser":7, "destroyer":10, "battleship":5, "carrier":5, "attack-submarine":15, "missile-submarine":15, "light-fighter":30, "heavy-fighter":15, "bomber":15, "stealth-bomber":10, "recon":20, "transport":30, "drone":30}
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
kamikazeTable = {"light-fighter":6, "heavy-fighter":8}
moveFireTable = {"infantry":1, "engineers":1, "mechanized":1, "light-cavalry":1, "med-cavalry":1, "heavy-cavalry":1, "special":1, "corvette":1, "amphibious":1, "patrol":1, "cruiser":1, "destroyer":1, "battleship":1, "carrier":1, "light-fighter":1, "heavy-fighter":1, "bomber":1, "stealth-bomber":1, "recon":4, "transport":1, "drone":1}
bombTable = {"bomber":8, "stealth-bomber":6, "drone":10}
flyTable = {"light-fighter":1, "heavy-fighter":1, "bomber":1, "stealth-bomber":1, "recon":1, "transport":1, "drone":1}
nukeTable = {"missile-submarine":30, "stealth-bomber":16}
structureTable = {}
manPages = {"score":"'score'", "turn":"'turn'", "details":"'details'", "quit":"'quit'", "help":"'help'", "health":"'health [unit] [value]'", "kill":"'kill [unit]'", "convert":"'convert [unit]'", "disable":"'disable [unit]'", "merge":"'merge [unit1] [unit2] ... > [unit]'", "split":"'split [unit] > [unit1] [unit2] ...'", "info":"'info [unit]'", "use":"'use [unit]'", "man":"'man [command]'", "attack":"'attack [unit1] [unit2] ... > [unit3] [unit4] ...'", "hide":"'hide [unit]'", "reveal":"'reveal [unit]'", "fire":"'fire [unit1] [unit2] ... > [unit3] [unit4] ...'", "heading":"'heading [unit]'", "torpedo":"'torpedo [unit] > [target]'", "sortie":"'sortie [unit] > [target]'", "depthcharge":"'depthcharge [unit] > [target]'", "board":"'board [unit] > [target]'", "missile":"'missile [unit] > [target]'", "takeoff":"'takeoff [unit]'", "land":"'land [unit]'", "kamikaze":"'kamikaze [unit] > [target]'", "dogfight":"'dogfight [unit1] [unit2] ... > [target1] [target2] ...'", "bomb":"'bomb [unit] > [target1] [target2] ...'", "survey":"'survey [unit]'", "pulse":"'pulse [unit] > [target1] [target2] ...'", "airlift":"'airlift [plane] > [unit]'", "nuke":"'nuke [unit] > [target]'", "message":"'message'", "move":"'move [unit]'", "spy": "'spy [unit]'", "build":"'build [unit]'"}

# initialization
from gamefiles.brandywine import *
firstHealth = sum(firstTeamTable.values())
secondHealth = sum(secondTeamTable.values())
loadGame()

# Meta-functions
def update():
    # update.globals
    global firstHealth
    global secondHealth
    global firstTeamTable
    global secondTeamTable
    # update.push
    firstHealth = sum(firstTeamTable.values())
    secondHealth = sum(secondTeamTable.values())

def error(code, function):
    print(errorMessages.get(code))
    print("Origin:", str(function))   

def reduce(unit):
    # reduce.definition
    export = 0
    # reduce.parse
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    # reduce.checks
    # reduce.checks.hillTerrain
    if locationTable.get(unit) == "hill": 
        # reduce.checks.hillTerrain.mechanized
        if unitType == "mechanized": 
            pass
        # reduce.checks.hillTerrain.special
        elif unitType == "special": 
            pass
        # reduce.checks.hillTerrain.remainder
        else: 
            export = export + 1
    # reduce.checks.forestTerrain
    elif locationTable.get(unit) == "forest":
        # reduce.checks.forestTerrain.infantry
        if unitType == "infantry": 
            pass
        # reduce.checks.forestTerrain.lightArtillery
        elif unitType == "light-artillery": 
            pass
        # reduce.checks.forestTerrain.medArtillery
        elif unitType == "med-artillery": 
            pass
        # reduce.checks.forestTerrain.heavyArtillery
        elif unitType == "heavy-artillery": 
            pass
        # reduce.checks.forestTerrain.special
        elif unitType == "special": 
            pass
        # reduce.checks.forestTerrain.remainder
        else: 
            export = export + 1
    # reduce.checks.swampTerrain
    elif locationTable.get(unit) == "swamp": 
        export = export + 1
    # reduce.checks.structure
    elif locationTable.get(unit) in structureTable: 
        export = structureTable.get(locationTable.get(unit))
    # reduce.push
    return int(export)

def fortificationReduce(structure, damage):
    # fortificationReduce.globals
    global structureTable
    # fortificationReduce.parse
    initialNetDamage = structureTable.get(structure) - damage
    # fortificaitonReduce.action
    # fortificationReduce.action.reduction
    if initialNetDamage > 0:
        structureTable[structure] = initialNetDamage
        print(structure, "new value:", str(initialNetDamage))
        return 0
    # fortificationReduce.action.destruction
    else:
        print(structure, "destroyed.")
        del structureTable[structure]
        finalNetDamage = abs(initialNetDamage)
        return finalNetDamage

def damage(unit, table):
    # damage.parse
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    # damage.checks
    # damage.checks.immobileUsed
    if unit in immobileUnits or unit in usedUnits:
        error("available", "damage.checks.immobileUsed")
        return
    # damage.checks.dead
    if unit in deadUnits:
        error("dead", "damage.checks.dead")
        return
    # damage.checks.functionAvailability
    if not unitType in table: 
        error("function", "damage.checks.functionAvailability")
        return
    # damage.action
    basicMaximum = table.get(unitType) + 1
    multiplier = dividedTable.get(unit, 1)
    maximum = basicMaximum * multiplier
    # damage.push
    return random.randrange(1, maximum)

def fog():
    # fog.checks
    if fogOfWar == 1: 
        return False
    # fog.action
    export = random.randrange(1, fogOfWar + 1)
    # fog.push
    # fog.push.fail
    if export == 1: 
        return True
    # fog.push.pass
    else: 
        return False

def kill(arguments):
    # kill.globals
    global firstTeamTable
    global secondTeamTable
    global firstTeamFlying
    global secondTeamTable
    global deadUnits
    # kill.parse
    # kill.parse.unit
    # kill.parse.unit.tooManyArguments
    if len(arguments) == 2: 
        unit = arguments[1]
    # kill.parse.unit.argument
    else: 
        unit = arguments
    # kill.parse.team
    # kill.parse.team.first
    if unit in firstTeamTable: 
        table = firstTeamTable
        flyingTable = firstTeamFlying
    # kill.parse.team.second
    elif unit in secondTeamTable: 
        table = secondTeamTable
        flyingTable = secondTeamFlying
    # kill.parse.team.none
    else: 
        error("unit", "kill.parse.team.none")
        return
    # kill.push
    del table[unit]
    if unit in flyingTable: 
        flyingTable.remove(unit)
    deadUnits.append(unit)
    # kill.return
    print(unit, "killed.")
    update()

def log():
    # log.definition
    originalOutput = sys.stdout
    # log.write
    with open("log.txt", "w") as f:
        # log.write.definition
        sys.stdout = f
        # log.write.header
        print("Round:", round)
        print("Command:", commandNumber)
        # log.write.team
        # log.write.team.first
        for x in firstTeamTable:
            # log.write.team.first.definition
            healthValue = firstTeamTable[x]
            originalValue = firstTeamTableOriginal[x]
            if healthValue == originalValue: continue
            # log.write.team.first.write
            print(x, ":", healthValue)
        # log.write.team.second
        for x in secondTeamTable:
            # log.write.team.second.definition
            healthValue = secondTeamTable[x]
            originalValue = secondTeamTableOriginal[x]
            if healthValue == originalValue: continue
            # log.write.team.second.write
            print(x, ":", healthValue)
        # log.write.lists
        print("")
        print("usedUnits =", usedUnits)
        print("immobileUnits =", immobileUnits)
        print("hiddenUnits =", hiddenUnits)
        print("disabledUnits =", disabledUnits)
        print("deadUnits =", deadUnits)
        print(secrets)
        score()
    # log.push
    sys.stdout = originalOutput

def dealDamage(unit, damage, teamTable):
    # dealDamage.globals
    global firstTeamTable
    global secondTeamTable
    # dealDamage.parse
    oldHealth = teamTable[unit]
    # dealDamage.action
    # dealDamage.action.kill
    if oldHealth - damage <= 0:
        kill(unit)
    # dealDamage.action.reduce
    else:
        newHealth = oldHealth - damage
        teamTable[unit] = newHealth
        print(unit, "new health:", newHealth)
    # dealDamage.return
    update()

def save():
    print("")
    print("firstTeam =", firstTeam)
    print("secondTeam =", secondTeam)
    print("campaign =", campaign)
    print("airTheater =", airTheater)
    print("fogOfWar =", fogOfWar)
    print("warheads =", warheads)
    print("firstTeamTable =", firstTeamTable)
    print("secondTeamTable =", secondTeamTable)
    print("locationTable =", locationTable)
    print("unitTable =", unitTable)
    print("allUnitTypes =", allUnitTypes)
    print("firstHealthTotal =", firstHealthTotal)
    print("secondHealthTotal =", secondHealthTotal)
    print("dividedTable =", dividedTable)
    print("hiddenUnits =", hiddenUnits)
    print("deadUnits =", deadUnits)
    print("")

# Umpire commands
def score():
    # score.definition
    update()
    # score.push
    firstPercent = firstHealth / firstHealthTotal * 100
    secondPercent = secondHealth / secondHealthTotal * 100
    # score.return
    print(firstTeam, "total health:", firstHealth, "or", firstPercent, "%")
    print(secondTeam, "total health:", secondHealth, "or", secondPercent, "%")

def turn():
    # turn.globals
    global round
    global airPhase
    global usedUnits
    global immobileUnits
    global alreadyDropped
    global disabledUnits
    # turn.action
    score()
    usedUnits.clear()
    immobileUnits.clear()
    alreadyDropped.clear()
    # turn.action.disabledUnits
    for x in disabledUnits: 
        immobileUnits.append(x)
        usedUnits.append(x)
    # turn.push
    disabledUnits.clear()
    round = round + 1
    airPhase = True

def details():
    print("Secrets:", secrets)
    print("Hidden units:", end = ": ")
    print(*hiddenUnits, sep = ", ")
    score()

def quitGame():
    areYouSure = input("Are you sure you want to quit? [Yes/no]: ")
    if areYouSure == "yes" or areYouSure == "y":
        score()
        quit()

def helpText():
    print("Commands:", helpTextBlock)
    print("Unit types:", end = ": ")
    print(*allUnitTypes.keys(), sep = ", ")

def health(arguments):
    # health.globals
    global firstTeamTable
    global secondTeamTable
    # health.parse
    # health.parse.unit
    # health.parse.unit.try
    try:
        unit = arguments[1]
    # health.parse.unit.except
    except:
        error("argument", "health.parse.unit.except")
        return
    # health.parse.health
    # health.parse.health.try
    try: 
        newHealth = float(arguments[2])
    # health.parse.health.except
    except:
        error("type", "health.parse.health.except")
        return
    # health.parse.team
    # health.parse.team.first
    if unit in firstTeamTable: 
        table = firstTeamTable
    # health.parse.team.second
    elif unit in secondTeamTable: 
        table = secondTeamTable
    # health.parse.team.none
    else:
        error("unit", "health.parse.team.none")
        return
    # health.action
    # health.action.kill
    if newHealth <= 0: 
        kill(arguments)
    # health.action.reduce
    else: 
        table[unit] = float(newHealth)
    # health.action.return
    score()

def freeze(arguments):
    # freeze.globals
    global immobileUnits
    # freeze.parse.unit
    # freeze.parse.unit.argument
    if len(arguments) == 1: 
        unit = str(arguments)
    # freeze.parse.unit.tooManyArguments
    else: 
        unit = arguments[1]
    # freeze.parse.team
    if not unit in firstTeamTable and not unit in secondTeamTable:
        error("unit", "freeze.parse.team")
        return
    # freeze.push
    immobileUnits.append(unit)

def use(arguments):
    # use.globals
    global usedUnits
    # use.parse.unit
    # use.parse.unit.argument
    if len(arguments) == 1: 
        unit = str(arguments)
    # use.parse.unit.tooManyArguments
    else: 
        unit = arguments
    # use.parse.team
    if not unit in firstTeamTable and not unit in secondTeamTable:
        error("unit", "use.parse.team")
        return
    # use.push
    usedUnits.append(unit)

def hide(arguments):
    # hide.globals
    global secrets
    global locationTable
    global hiddenUnits
    # hide.parse
    # hide.parse.unit
    # hide.parse.unit.argument
    if len(arguments) == 1: 
        unit = arguments
    # hide.parse.unit.tooManyArguments
    else: 
        unit = arguments[1]
    # hide.parse.argument
    # hide.parse.argument.try
    try:
        localUnitType = unitTable.get(unit)
    # hide.parse.argument.except
    except:
        error("argument", "hide.parse.argument.except")
        return
    # hide.parse.type
    unitType = allUnitTypes.get(localUnitType)
    # hide.checks
    # hide.checks.type
    if not unitType in hideTable:
        error("function", "hide.checks.type")
        return
    # hide.checks,hidden
    if unit in hiddenUnits:
        error("hidden", "hide.checks.hidden")
        return
    # hide.action
    # hide.action.structure
    structure = input("Structure to hide in, if any: ")
    if structure in structureTable:
        # hide.action.structure.definition
        locationTable[unit] = structure
        # hide.action.structure.action
        hiddenUnits.append(unit)
        newSecret = unit + " hidden inside " + structure
        secrets = secrets + ", " + newSecret
        return
    # hide.action.terrain
    terrain = input("Terrain to hide in: ")
    if not terrain in hideableTerrain:
        error("terrain", "hide.action.terrain")
        return
    # hide.push
    hiddenUnits.append(unit)
    locationTable[unit] = terrain
    location = input("Location of this hidden unit: ")
    newSecret = unit + " hidden at " + location
    secrets = secrets + ", " + newSecret

def reveal(arguments):
    # reveal.globals
    global secrets
    global locationTable
    global hiddenUnits
    # reveal.parse
    # reveal.parse.unit
    # reveal.parse.unit.argument
    if len(arguments) == 1: 
        unit = arguments
    # reveal.parse.unit.tooManyArguments
    else: 
        unit = arguments[1]
    # reveal.parse.argument
    # reveal.parse.argument.try
    try:
        localUnitType = unitTable.get(unit)
    # reveal.parse.argument.except
    except:
        error("argument", "reveal.parse.argument.except")
        return
    # reveal.parse.type
    unitType = allUnitTypes.get(localUnitType)
    # reveal.checks
    # reveal.checks.type
    if not unit in hiddenUnits or not unitType in hideTable:
        error("function", "reveal.checks.type")
        return
    # reveal.action
    newLocation = input("New terrain: ")
    # reveal.push
    locationTable[unit] = newLocation
    hiddenUnits.remove(unit)
    newSecret = unit + " is no longer hidden."
    secrets = secrets + ", " + newSecret

def convert(arguments, teamTable):
    # convert.globals
    global firstTeamTable
    global secondTeamTable
    global unitTable
    # convert.parse
    # convert.parse.unit
    # convert.parse.unit.try
    try:
        unit = arguments[1]
    # convert.parse.unit.except
    except:
        error("argument", "convert.parse.unit.except")
        return
    # convert.parse.type
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    # convert.checks
    # convert.checks.function
    if not unitType in convertTable:
        error("function", "convert.checks.function")
        return
    # convert.checks.team
    if not unit in teamTable:
        error("team", "convert.checks.team")
        return
    # convert.action
    currentHealth = teamTable.get(unit)
    if currentHealth > 4: newHealth = 4
    else: newHealth = currentHealth
    # convert.push
    teamTable[unit] = newHealth
    unitTable[unit] = "infantry"
    update()

def disable(arguments):
    # disable.globals
    global disabledUnits
    global usedUnits
    global immobileUnits
    # disable.parse
    # disable.parse.argument
    if len(arguments) == 1: 
        unit = arguments
    # disable.parse.tooManyArguments
    else: 
        unit = arguments[1]
    # disable.push
    immobileUnits.append(unit)
    usedUnits.append(unit)
    disabledUnits.append(unit)

def merge(arguments, teamTable):
    # merge.globals
    global firstTeamTable
    global secondTeamTable
    global unitTable
    global dividedTable
    global usedUnits
    global immobileUnits
    global disabledUnits
    # merge.parse
    del arguments[0]
    # merge.parse.try
    try:
        mergedLocalUnitType = unitTable.get(arguments[0])
    # merge.parse.except
    except:
        error("argument", "merge.parse.except")
        return
    # merge.definition
    mergedUnitType = allUnitTypes.get(mergedLocalUnitType)
    totalHealth = 0
    numberOfUnits = 0
    mergedUnits = []
    finalUnit = ""
    immobile = False
    disabled = False
    used = False
    hidden = False
    # merge.action
    for x in arguments:
        # merge.action.exists
        if x in teamTable:
            # merge.action.exists.correctType
            if unitTable[x] == mergedUnitType:
                # merge.action.exists.correctType.update
                numberOfUnits = numberOfUnits + 1
                totalHealth = totalHealth + teamTable[x]
                mergedUnits.append(x)
                # merge.action.exists.correctType.immobile
                if x in immobileUnits: 
                    immobile = True
                # merge.action.exists.correctType.disabled
                if x in disabledUnits: 
                    disabled = True
                # merge.action.exists.correctType.used
                if x in usedUnits: 
                    used = True
                # merge.action.exists.correctType.hidden
                if x in hiddenUnits: 
                    hidden = True
            # merge.action.exists.wrongType
            else:
                print(x, "could not be merged.")
        # merge.action.redirect
        elif x == ">": pass
        # merge.action.doesNotExist
        else:
            # merge.action.doesNotExist.wrongTeam
            if x in unitTable:
                error("exists", "merge.action.doesNotExist.wrongTeam")
                return
            # merge.action.doesNotExist.newUnit
            finalUnit = x
            break
    teamTable[finalUnit] = totalHealth
    unitTable[finalUnit] = mergedUnitType
    dividedTable[finalUnit] = numberOfUnits
    # merge.push
    # merge.push.clear
    for x in mergedUnits: 
        del teamTable[x]
        del unitTable[x]
    # merge.push.append
    # merge.push.append.immobile
    if immobile == True: 
        immobileUnits.append(finalUnit)
    # merge.push.append.used
    if used == True: 
        usedUnits.append(finalUnit)
    # merge.push.append.disabled
    if disabled == True: 
        immobileUnits.append(finalUnit)
        disabledUnits.append(finalUnit)
        usedUnits.append(finalUnit)
    # merge.push.append.hidden
    if hidden == True: 
        hiddenUnits.append(finalUnit)

def split(arguments, teamTable):
    # split.globals
    global firstTeamTable
    global secondTeamTable
    global dividedTable
    global unitTable
    global usedUnits
    global immobileUnits
    global disabledUnits
    # split.parse
    del arguments[0]
    # split.parse.try
    try:
        originalUnit = arguments[0]
    # split.parse.except
    except:
        error("argument", "split")
        return
    # split.definition
    localUnitType = unitTable.get(originalUnit)
    unitType = allUnitTypes.get(localUnitType)
    numberOfUnits = 0
    newUnits = []
    currentHealth = teamTable.get(originalUnit)
    # split.checks
    if not originalUnit in dividedTable or not unitType in splitTable:
        error("function", "split.checks")
        return
    # split.action
    # split.action.originals
    for x in arguments:
        # split.action.originals.exists
        if x in teamTable: 
            pass
        # split.action.originals.redirect
        elif x == ">": 
            pass
        # split.action.originals.doesNotExist
        else:
            # split.action.originals.doesNotExist.wrongTeam
            if x in unitTable:
                print(x, "could not be created.")
                return
            # split.action.originals.doesNotExist.newUnit
            else:
                numberOfUnits = numberOfUnits + 1
                newUnits.append(x)
    # split.action.health
    newHealth = currentHealth / numberOfUnits
    # split.action.new
    for x in newUnits:
        # split.action.new.parse
        teamTable[x] = newHealth
        unitTable[x] = unitType
        # split.action.new.append
        # split.action.new.append.immobile
        if originalUnit in immobileUnits: 
            immobileUnits.append(x)
        # split.action.new.append.disabled
        if originalUnit in disabledUnits:
            immobileUnits.append(x)
            disabledUnits.append(x)
            usedUnits.append(x)
        # split.action.new.append.used
        if originalUnit in usedUnits: 
            usedUnits.append(x)
        # split.action.new.append.hidden
        if originalUnit in hiddenUnits: 
            hiddenUnits.append(x)
        # split.action.new.newHealth
        dividedTable[x] = 1 / numberOfUnits
    # split.push
    # split.push.tables
    del teamTable[originalUnit]
    del unitTable[originalUnit]
    if originalUnit in dividedTable: 
        del dividedTable[originalUnit]
    # split.push.immobile 
    if originalUnit in immobileUnits: 
        immobileUnits.remove(originalUnit)
    # split.push.disabled
    if originalUnit in disabledUnits: 
        disabledUnits.remove(originalUnit)
        hiddenUnits.remove(originalUnit)
    # split.push.used
    if originalUnit in usedUnits: 
        usedUnits.remove(originalUnit)
    # split.push.hidden
    if originalUnit in hiddenUnits: 
        hiddenUnits.remove(originalUnit)      

def man(arguments):
    # man.checks
    # man.checks.arguments
    # man.checks.arguments.try
    try:
        command = arguments[1]
    # man.checks.arguments.except
    except:
        error("argument", "man.checks.arguments.except")
        return
    # man.checks.command
    if not str(command) in manPages:
        error("command", "man.checks.command")
        print("Type 'help' for a list of commands.")
        return
    # man.return
    print(manPages.get(command))

def message():
    # message.action
    test = fog()
    # message.return
    # message.return.failed
    if test == True:
        print("Message failed to deliver.")
        return
    # message.return.passed
    else:
        print("Message delivered.")

# Theater-agnostic functions
def attack(arguments, teamTable, targetTeamTable):
    global usedUnits
    global hiddenUnits
    global immobileUnits
    totalAttackDamage = 0
    totalDefenseDamage = 0
    defendingUnits = []
    del arguments[0]
    for x in arguments:
        if x == ">": 
            pass
        elif x in teamTable:
            if x in usedUnits: 
                continue
            initialDamage = damage(x, attackTable)
            if initialDamage == None: 
                continue
            if reduce(x) == 0: 
                finalDamage = initialDamage
            else: 
                finalDamage = initialDamage - reduce(x)
            totalAttackDamage = totalAttackDamage + finalDamage
            if x in hiddenUnits: 
                hiddenUnits.remove(x)
            usedUnits.append(x)
            localUnitType = unitTable.get(x)
            unitType = allUnitTypes.get(localUnitType)
            if not unitType in moveFireTable: 
                immobileUnits.append(x)
        elif x in targetTeamTable:
            initialDefense = damage(x, attackTable)
            if initialDefense == None: 
                continue
            totalDefenseDamage = totalDefenseDamage + initialDefense
            defendingUnits.append(x)
            if x in hiddenUnits: 
                hiddenUnits.remove(x)
            usedUnits.append(x)
            localUnitType = unitTable.get(x)
            unitType = allUnitTypes.get(localUnitType)
            if not unitType in moveFireTable: 
                immobileUnits.append(x)
        else: print(x, " does not exist.")
    if totalDefenseDamage >= totalAttackDamage:
        print("Attack repelled.")
        return
    netDamage = totalAttackDamage - totalDefenseDamage
    print("Net damage: ", netDamage)
    perUnitDamage = netDamage / len(defendingUnits)
    print("Damage per unit:", perUnitDamage)
    for x in defendingUnits:
        location = locationTable.get(x)
        if location in structureTable:
            reducedDamage = fortificationReduce(location, perUnitDamage)
        else: 
            reducedDamage = perUnitDamage
        dealDamage(x, reducedDamage, targetTeamTable)
    defendingUnits.clear()
    turn()

def move(arguments, teamTable):
    global locationTable
    global immobileUnits
    global usedUnits
    try:
        unit = arguments[1]
    except:
        error("argument", "move")
        return
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    if not unit in teamTable:
        error("team", "move")
        return
    if unit in immobileUnits:
        error("available", "move")
        return
    if unitType in headingTable:
        error("heading", "move")
    if not unitType in moveFireTable:
        usedUnits.append(unit)
    currentLocation = locationTable.get(unit)
    print("Current location or terrain:", currentLocation)
    newLocation = input("New location or terrain: ")
    if unit in hiddenUnits:
        if not newLocation in structureTable or not newLocation in hideableTerrain:
            usedUnits.remove(unit)
    locationTable[unit] = str(newLocation)
    immobileUnits.append(unit)

def spy(arguments, teamTable):
    global usedUnits
    try:
        unit = arguments[1]
    except:
        error("argument", "spy")
        return
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    if not unit in teamTable:
        error("team", "spy")
        return
    if unit in usedUnits:
        error("available", "spy")
        return
    if not unitType in spyTable:
        error("function", "spy")
        return
    effectiveness = damage(unit, spyTable)
    if effectiveness >= 6: 
        print("Good information.")
    elif effectiveness == 1: 
        print("Bad information.")
    else: 
        print("No information.")
    details()
    usedUnits.append(unit)

def fire(arguments, teamTable, targetTeamTable):
    global usedUnits
    global immobileUnits
    del arguments[0]
    totalAttackDamage = 0
    defendingUnits = []
    for x in arguments:
        if x == ">": 
            pass
        elif x in teamTable:
            if x in usedUnits: 
                continue
            initialDamage = damage(x, fireTable)
            if initialDamage == None: 
                continue
            totalAttackDamage = initialDamage + totalAttackDamage
            usedUnits.append(x)
            localUnitType = unitTable.get(x)
            unitType = allUnitTypes.get(localUnitType)
            if not unitType in moveFireTable: 
                immobileUnits.append(x)
            if x in hiddenUnits: 
                reveal(x)
        elif x in targetTeamTable:
            defendingUnits.append(x)
        else: 
            print(x, " does not exist.")
            return
    print("Damage:", totalAttackDamage)
    try:
        perUnitDamage = totalAttackDamage / len(defendingUnits)
    except:
        error("argument", "fire")
        return
    print("Damage per unit:", perUnitDamage)
    for x in defendingUnits:
        location = locationTable.get(x)
        if location in structureTable:
            reducedDamage = fortificationReduce(location, perUnitDamage)
        else: 
            reducedDamage = perUnitDamage
        dealDamage(x, reducedDamage, targetTeamTable)
    defendingUnits.clear()
    score()

# Naval functions
def heading(arguments, teamTable):
    global immobileUnits
    global usedUnits
    try:
        unit = arguments[1]
    except:
        error("argument", "heading")
        return
    if not unit in teamTable:
        error("team", "convert")
        return
    if unit in usedUnits or unit in immobileUnits:
        error("available", "heading")
        return
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    if not unitType in headingTable:
        error("required", "heading")
        return
    immobileUnits.append(unit)
    if not unitType in moveFireTable: 
        usedUnits.append(unit)

def torpedo(arguments, teamTable, targetTeamTable):
    global usedUnits
    global immobileUnits
    del arguments[0]
    try:
        unit = arguments[0]
    except:
        error("argument", "torpedo")
        return
    if not unit in teamTable:
        error("team", "torpedo")
        return
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    if unit in immobileUnits or unit in usedUnits:
        error("available", "torpedo")
        return
    if not unitType in torpedoTable:
        error("function", "torpedo")
        return
    effectiveness = 0
    target = ""
    for x in arguments:
        if x == ">": 
            pass
        elif x in teamTable: 
            effectiveness = damage(x, torpedoTable)
        elif x in targetTeamTable: 
            target = x
        else: 
            print(x, "does not exist.")
            return
    oldHealth = targetTeamTable.get(target)
    if effectiveness == 6 or oldHealth - effectiveness <= 0:   
        kill(target)
    else:
        newHealth = oldHealth - effectiveness
        targetTeamTable[target] = newHealth
    usedUnits.append(unit)
    immobileUnits.append(unit)
    if unit in hiddenUnits: 
        reveal(unit)
    score()

def sortie(arguments, teamTable, targetTeamTable):
    global usedUnits
    global immobileUnits
    del arguments[0]
    try:
        unit = arguments[0]
    except:
        error("argument", "sortie")
        return
    if not unit in teamTable:
        print("team", "sortie")
        return
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    if unit in usedUnits:
        error("available", "sortie")
        return
    if not unitType in sortieTable:
        error("function", "sortie")
        return
    attackDamage = 0
    defenseDamage = 0
    defendingUnits = []
    for x in arguments:
        if x == ">": 
            pass
        elif x in teamTable: 
            attackDamage = damage(x, sortieTable)
        elif x in targetTeamTable: 
            defenseDamage = damage(x, sortieDefenseTable)
            defendingUnits.append(x)
        else: 
            print(x, "does not exist.")
            return
    if defenseDamage >= attackDamage: 
        print("Sortie repelled.")
    else:
        netDamage = attackDamage - defenseDamage
        perUnitDamage = netDamage / len(defendingUnits)
        for x in defendingUnits:
            if x in hiddenUnits: 
                reveal(x)
            dealDamage(defendingUnits, perUnitDamage, targetTeamTable)
    usedUnits.append(unit)
    score()

def depthcharge(arguments, teamTable, targetTeamTable):
    global firstTeamTable
    global secondTeamTable
    global alreadyDropped
    global usedUnits
    global immobileUnits
    global disabledUnits
    del arguments[0]
    try:
        unit = arguments [0]
    except:
        error("argument", "depthcharge")
        return
    if not unit in teamTable:
        error("team", "depthcharge")
        return
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    if unit in alreadyDropped:
        error("available", "depthcharge")
        return
    if not unitType in depthchargeTable:
        error("function", "depthcharge")
        return
    for x in arguments:
        if x == ">": 
            pass
        elif x in teamTable: 
            effectiveness = damage(x, depthchargeTable)
        elif x in targetTeamTable: 
            target = x
        else: 
            print(x, "does not exist.")
            return
    if effectiveness == 6: 
        kill(target)
    elif effectiveness == 5:
        print(target, "disabled.")
        immobileUnits.append(target)
        disabledUnits.append(target)
        usedUnits.append(target)
    else: print("Missed.")
    immobileUnits.append(unit)
    alreadyDropped.append(unit)
    score()

def board(arguments, teamTable, targetTeamTable):
    global firstTeamTable
    global secondTeamTable
    global usedUnits
    global immobileUnits
    global disabledUnits
    del arguments[0]
    try:
        unit = arguments[0]
    except:
        error("argument", "board")
        return
    if not unit in teamTable:
        error("team", "depthcharge")
        return
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    currentHealth = teamTable.get(unit)
    if unit in usedUnits:
        error("available", "board")
        return
    if not unitType in boardTable:
        error("function", "board")
        return
    for x in arguments:
        if x == ">": 
            pass
        elif x in teamTable: 
            effectiveness = damage(x, boardTable)
        elif x in targetTeamTable: 
            target = x
        else: 
            print(x, "does not exist.")
            return
    if effectiveness >= 5:
        print(target, "seized.")
        targetHealth = targetTeamTable.get(target)
        del targetTeamTable[target]
        teamTable[target] = targetHealth
        immobileUnits.append(unit)
    else:
        print("Seizure failed.")
        print(unit, "suffers", str(effectiveness), "damage.")
        if currentHealth - effectiveness <= 0:
            kill(unit)
        else:
            newHealth = currentHealth - effectiveness
            teamTable[unit] = newHealth
        immobileUnits.append(unit)
        disabledUnits.append(unit)
        usedUnits.append(unit)
    usedUnits.append(unit)
    score()

def nuke(arguments, teamTable, targetTeamTable):
    global firstTeamTable
    global secondTeamTable
    global warheads
    global usedUnits
    global immobileUnits
    global disabledUnits
    del arguments[0]
    try:
        unit = arguments[0]
    except:
        error("argument", "nuke")
        return
    target = arguments[2]
    if not unit in teamTable:
        error("team", "nuke")
        return
    if not target in targetTeamTable:
        error("team", "nuke")
        return
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    if unit in usedUnits:
        error("available", "nuke")
        return
    if not unitType in nukeTable:
        error("function", "nuke")
        return
    if warheads <= 0:
        print("Not enough warheads.")
        return
    warheads = warheads - 1
    principalDamage = damage(unit, nukeTable)
    dealDamage(target, principalDamage, targetTeamTable)
    halfDamageRawUnits = input("Units or structures within 7 cm: ")
    halfDamageUnits = halfDamageRawUnits.split()
    halfDamage = principalDamage / 2
    for x in halfDamageUnits:
        if x in structureTable: 
            fortificationReduce(x, halfDamage)
        elif x in targetTeamTable: 
            dealDamage(x, halfDamage, targetTeamTable)
        else: 
            print(x, "is not a structure or a unit.")
    quarterDamageRawUnits = input("Units or structures within 15 cm: ")
    quarterDamageUnits = quarterDamageRawUnits.split()    
    quarterDamage = principalDamage / 4
    for x in quarterDamageUnits:
        if x in structureTable: 
            fortificationReduce(x, quarterDamage)
        elif x in targetTeamTable: 
            dealDamage(x, quarterDamage, targetTeamTable)
        else: 
            print(x, "is not a structure or a unit.")
    immobileUnits.append(unit)
    disabledUnits.append(unit)
    usedUnits.append(unit)

# Army functions
def build(arguments, teamTable):
    global structureTable
    global usedUnits
    global immobileUnits
    del arguments[0]
    try:
        unit = arguments[0]
    except:
        error("argument", "build")
        return
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    if not unit in teamTable:
        error("team", "convert")
        return
    if unit in usedUnits:
        error("available", "build")
        return
    if not unitType in buildTable:
        error("function", "build")
        return
    strength = damage(unit, buildTable)
    structure = input("Name of new structure:")
    while structure in structureTable:
        print("A structure with that name already exists.")
        structure = input("Name of new structure:")
    structureTable[structure] = strength
    print(structure, "has strength:", strength)
    usedUnits.append(unit)
    if not unitType in moveFireTable: immobileUnits.append(unit)

def missile(arguments, teamTable, targetTeamTable):
    global firstTeamTable
    global secondTeamTable
    global usedUnits
    global immobileUnits
    try:
        foo = arguments[1]
    except:
        error("argument", "missile")
        return
    del arguments[0]
    for x in arguments:
        if x == ">": 
            pass
        elif x in teamTable: 
            unit = x
            if x in hiddenUnits: reveal(x)
            usedUnits.append(x)
        elif x in targetTeamTable: 
            target = x
        else: 
            print(x, "does not exist.")
            return
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    if unit in usedUnits:
        error("available", "missile")
        return
    if not unitType in missileTable:
        error("function", "missile")
        return
    attackDamage = damage(unit, missileTable)
    localTargetUnitType = unitTable.get(target)
    targetUnitType = allUnitTypes.get(localTargetUnitType)
    targetLocation = locationTable.get(target)
    if targetUnitType in missileTable:
        defenseDamage = damage(target, missileTable)
        if defenseDamage >= attackDamage:
            print("Missile repelled.")
            return
        else: 
            netDamage = attackDamage - defenseDamage
    else: 
        netDamage = attackDamage
    if targetLocation in structureTable:
        finalDamage = fortificationReduce(targetLocation, netDamage)
    else: 
        finalDamage = netDamage
    dealDamage(target, finalDamage, targetTeamTable)
    usedUnits.append(unit)
    score()

# Air functions
def takeoff(arguments):
    global firstTeamFlying
    global secondTeamFlying
    global usedUnits
    global immobileUnits
    try:
        unit = arguments[1]
    except:
        error("argument", "takeoff")
        return
    if unit in firstTeamTable: 
        teamFlyingTable = firstTeamFlying
    elif unit in secondTeamTable: 
        teamFlyingTable = secondTeamFlying
    else:
        error("unit", "takeoff")
        return
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    if unit in usedUnits:
        error("available", "takeoff")
        return
    if not unitType in flyTable:
        error("function", "takeoff")
        return
    if unit in teamFlyingTable:
        print("Already airborne.")
        return
    teamFlyingTable.append(unit)
    if unitType in hideTable:
        hide(unit)

def land(arguments):
    global firstTeamFlying
    global secondTeamFlying
    global usedUnits
    if len(arguments) == 2: 
        unit = arguments[1]
    else: 
        unit = arguments
    if unit in firstTeamTable: 
        teamFlyingTable = firstTeamFlying
    elif unit in secondTeamTable: 
        teamFlyingTable = secondTeamFlying
    else:
        error("unit", "land")
        return
    try:
        localUnitType = unitTable.get(unit)
    except:
        error("argument", "land")
        return
    unitType = allUnitTypes.get(localUnitType)
    if not unitType in flyTable:
        error("function", "land")
        return
    if not unit in teamFlyingTable:
        error("airborne", "land")
        return
    teamFlyingTable.remove(unit)
    usedUnits.append(unit)

def pulse(arguments, teamTable, targetTeamTable, teamFlyingTable):
    global usedUnits
    global immobileUnits
    global disabledUnits
    try:
        foo = arguments[1]
    except:
        error("argument", "pulse")
        return
    del arguments[0]
    defendingUnits = []
    for x in arguments:
        if x == ">": 
            pass
        elif x in teamTable:
            if x in teamFlyingTable:
                unit = x
            else: 
                print(x, "is not airborne.")
        elif x in targetTeamTable:
            defendingUnits.append(x)
        else: 
            print(x, "does not exist.")
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    if unitType in usedUnits:
        error("available", "pulse")
        return
    if not unitType in pulseTable:
        error("function", "pulse")
        return
    effectiveness = damage(unit, pulseTable)
    effectiveness = 6
    if effectiveness == 6:
        print("Pulse effective.")
        for x in defendingUnits: 
            immobileUnits.append(x)
            disabledUnits.append(x)
            usedUnits.append(x)
    else:
        print("Pulse ineffective.")
    usedUnits.append(unit)

def airlift(arguments, teamTable, teamFlyingTable):
    global locationTable
    global usedUnits
    global immobileUnits
    try:
        foo = arguments[1]
    except:
        error("argument", "airlift")
        return
    del arguments[0]
    liftedUnits = []
    for x in arguments:
        if x == ">": pass
        elif x in teamTable:
            if x in teamFlyingTable:
                unit = x
            else:
                liftedLocalUnitType = unitTable.get(x)
                liftedUnitType = allUnitTypes.get(liftedLocalUnitType)
                if not liftedUnitType in airliftTable:
                    print(x, "cannot be airlifted.")
                    return
                liftedUnits.append(x)
        else: 
            print(x, "does not exist, or does not belong to you.")
            return
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    if unit in usedUnits:
        error("available", "airlift")
        return
    if unitType != "transport":
        error("function", "airlift")
        return
    for x in liftedUnits:
        currentLocation = locationTable.get(x)
        print("Current location or terrain: ", currentLocation)
        newLocation = input("New location or terrain: ")
        if x in hiddenUnits:
            if not newLocation in structureTable or not newLocation in hideableTerrain:
                reveal(x)
        locationTable[x] = str(newLocation)
    usedUnits.append(unit)

def kamikaze(arguments, teamTable, targetTeamTable, teamFlyingTable):
    global usedUnits
    try:
        foo = arguments[1]
    except:
        error("argument", "kamikaze")
        return
    del arguments[0]
    for x in arguments:
        if x == ">": 
            pass
        elif x in teamTable:
            if not x in teamFlyingTable:
                error("airborne", "kamikaze")
                return
            else:
                unit = x
        elif x in targetTeamTable: 
            target = x
        else: 
            print(x, "does not exist.")
            return
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    if unit in usedUnits:
        error("available", "kamikaze")
        return
    if not unitType in kamikazeTable:
        error("function", "kamikaze")
        return
    effectiveness = damage(unit, kamikazeTable)
    if effectiveness == 6: 
        kill(target)
    else: 
        dealDamage(target, effectiveness, targetTeamTable)
    kill(unit)
    score()

def air_missile(arguments, teamTable, targetTeamTable, teamFlyingTable):
    global firstTeamTable
    global secondTeamTable
    global usedUnits
    try:
        foo = arguments[1]
    except:
        error("argument", "air-missile")
        return
    for x in arguments:
        if x in teamTable: 
            unit = str(x)
        elif x in targetTeamTable: 
            target = str(x)
        else:
            if x == ">" or x == "missile": continue
            if not x in unitTable:
                error("unit", "air-missile")
                return
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    if unit in usedUnits:
        error("available", "air-missile")
        return
    if not unitType in missileTable:
        error("function", "air-missile")
        return
    if not unit in teamFlyingTable:
        error("airborne", "air-missile")
        return
    attackDamage = damage(unit, missileTable)
    localTargetUnitType = unitTable.get(target)
    targetUnitType = allUnitTypes.get(localTargetUnitType)
    targetLocation = locationTable.get(target)
    if targetUnitType in missileTable:
        defenseDamage = damage(target, missileTable)
        if defenseDamage >= attackDamage:
            print("Missile repelled.")
            return
        else: 
            netDamage = attackDamage - defenseDamage
    else: 
        netDamage = attackDamage
    if targetLocation in structureTable:
        finalDamage = fortificationReduce(targetLocation, netDamage)
    else: 
        finalDamage = netDamage
    dealDamage(target, finalDamage, targetTeamTable)
    usedUnits.append(unit)
    score()

def dogfight(arguments, teamTable, targetTeamTable, teamFlyingTable, targetTeamFlyingTable):
    global usedUnits
    global immobileUnits
    totalAttackDamage = 0
    totalDefenseDamage = 0
    defendingUnits = []
    try:
        foo = arguments[1]
    except:
        error("argument", "dogfight")
        return
    del arguments[0]
    for x in arguments:
        if x == ">": pass
        elif x in teamTable:
            if not x in teamFlyingTable:
                print(x, "is not airborne.")
                continue
            if x in usedUnits: 
                continue
            initialDamage = damage(x, attackTable)
            if initialDamage == None: 
                continue
            if reduce(x) == 0: 
                finalDamage = initialDamage
            else: 
                finalDamage = initialDamage - reduce(x)
            totalAttackDamage = totalAttackDamage + finalDamage
            if x in hiddenUnits: 
                reveal(x)
            usedUnits.append(x)
            localUnitType = unitTable.get(x)
            unitType = allUnitTypes.get(localUnitType)
            if not unitType in moveFireTable: 
                immobileUnits.append(x)
        elif x in targetTeamTable:
            if not x in targetTeamFlyingTable:
                print(x, "is not airborne.")
                continue
            initialDefense = damage(x, attackTable)
            if initialDefense == None: 
                continue
            totalDefenseDamage = totalDefenseDamage + initialDefense
            defendingUnits.append(x)
            if x in hiddenUnits: 
                reveal(x)
            usedUnits.append(x)
            localUnitType = unitTable.get(x)
            unitType = allUnitTypes.get(localUnitType)
            if not unitType in moveFireTable: 
                immobileUnits.append(x)
        else: 
            print(x, " does not exist.")
    if totalDefenseDamage >= totalAttackDamage:
        print("Attack repelled.")
        return
    netDamage = totalAttackDamage - totalDefenseDamage
    print("Net damage: ", netDamage)
    perUnitDamage = netDamage / len(defendingUnits)
    print("Damage per unit:", perUnitDamage)
    for x in defendingUnits:
        dealDamage(defendingUnits, perUnitDamage, targetTeamTable)
    defendingUnits.clear()
    turn()

def bomb(arguments, teamTable, targetTeamTable, teamFlyingTable):
    global usedUnits
    global immobileUnits
    try:
        foo = arguments[1]
    except:
        error("argument", "bomb")
        return
    del arguments[0]
    totalAttackDamage = 0
    defendingUnits = []
    for x in arguments:
        if x == ">": 
            pass
        elif x in teamTable:
            if not x in teamFlyingTable:
                error("airborne")
                return
            if x in usedUnits: 
                continue
            initialDamage = damage(x, fireTable)
            if initialDamage == None: 
                continue
            totalAttackDamage = initialDamage + totalAttackDamage
            usedUnits.append(x)
            localUnitType = unitTable.get(x)
            unitType = allUnitTypes.get(localUnitType)
            if not unitType in moveFireTable: 
                immobileUnits.append(x)
            if x in hiddenUnits: 
                reveal(x)
        elif x in targetTeamTable:
            defendingUnits.append(x)
        else: 
            print(x, " does not exist.")
    print("Damage:", totalAttackDamage)
    perUnitDamage = totalAttackDamage / len(defendingUnits)
    print("Damage per unit:", perUnitDamage)
    for x in defendingUnits:
        location = locationTable.get(x)
        if location in structureTable:
            reducedDamage = fortificationReduce(location, perUnitDamage)
        else: 
            reducedDamage = perUnitDamage
        dealDamage(defendingUnits, reducedDamage, targetTeamTable)
    defendingUnits.clear()
    score()

def survey(arguments, teamTable, teamFlyingTable):
    global usedUnits
    try:
        unit = arguments[1]
    except:
        error("argument", "survey")
        return
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    if not unit in teamTable:
        error("team", "survey")
        return
    if unit in usedUnits:
        error("available", "survey")
        return
    if not unitType in spyTable:
        error("function", "survey")
        return
    if not unit in teamFlyingTable:
        error("airborne", "survy")
    effectiveness = damage(unit, spyTable)
    if effectiveness >= 6: 
        print("Good information.")
    elif effectiveness == 1: 
        print("Bad information.")
    else: 
        print("No information.")
    details()
    usedUnits.append(unit)

# Shell functions

def info(arguments):
    try:
        unit = arguments[1]
    except:
        error("argument", "info")
        return
    print(unit, "attributes:")
    print("")
    if unit in firstTeamTable: 
        print("Affiliation:", firstTeam)
        teamTable = firstTeamTable
    elif unit in secondTeamTable: 
        print("Affiliation:", secondTeam)
        teamTable = secondTeamTable
    elif unit in deadUnits: print("Dead.")
    else:
        print("No such unit.")
        return
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    print("Local unit type:", localUnitType)
    print("Universal unit type:", unitType)
    print("")
    print("Current health:", teamTable.get(unit))
    healthPercentage = teamTable.get(unit) / healthTable.get(unitType) * 100
    print("Health percentage:", healthPercentage, "%")
    if unit in locationTable:
        location = locationTable.get(unit)
        print("Current location:", location)
        if location in structureTable: print("Current structure strength:", structureTable.get(location))
    if unit in usedUnits or unit in alreadyDropped: print("Used this turn.")
    if unit in immobileUnits: print("Immobile this turn.")
    else: print("Movement range:", movementTable.get(unitType))
    if unit in dividedTable: print("Size multiplier:", dividedTable.get(unit))
    print("")
    if unit in hiddenUnits: print("Hidden, type 'details' for more.")
    else:
        if unitType in hideTable: print("Hideable.")
    if unit in firstTeamFlying or unit in secondTeamFlying: print("Airborne.")
    if unitType in convertTable: print("Convertible to infantry.")
    if unitType in spyTable: print("Can spy.")
    if unitType in splitTable or unit in dividedTable: print("Divisible.")
    if unitType in headingTable: print("Cannot change heading more than 45 degrees in a turn.")
    if unitType in torpedoTable: print("Can fire torpedoes.")
    if unitType in depthchargeTable: print("Can drop depthcharges.")
    if unitType in boardTable: print("Can attempt to commandeer ships.")
    if unitType in pulseTable: print("Can drop electromagnetic pulses.")
    if unitType == "transport": print("Can transport other units.")
    if unitType in moveFireTable: print("Can move and fire in the same turn.")
    if unitType in flyTable: print("Airplane.")
    print("")
    if unitType in attackTable: print("Maximum attack damage:", attackTable.get(unitType))
    if unitType in fireTable: print("Maximum artillery damage:", fireTable.get(unitType))
    if unitType in missileTable: print("Maximum missile damage:", missileTable.get(unitType))
    if unitType in bombTable: print("Maximum bomb damage:", bombTable.get(unitType))
    if unitType in sortieTable: print("Maximum sortie damage:", sortieTable.get(unitType))
    if unitType in sortieDefenseTable: print("Maximum sortie defense:", sortieDefenseTable.get(unitType))
    if unitType in buildTable: print("Maximum built structure strength:", buildTable.get(unitType))
    if unitType in kamikazeTable: print("Maximum kamikaze damage:", kamikazeTable.get(unitType))
    if unitType in nukeTable: print("Maximum nuke damage:", nukeTable.get(unitType))

def airShell(team, teamTable, targetTeamTable, teamFlyingTable, targetTeamFlyingTable):
    global airPhase
    global commandNumber
    prompt = str(round) + " ~ " + str(commandNumber) + " " + str(campaign) + "-Air: " + str(team) + " % "
    rawCommand = input(prompt)
    parsedCommand = rawCommand.split()
    if fog() == True:
        print("This command fails.")
        commandNumber = commandNumber + 1
        return
    if not parsedCommand:
        error("command", "air-shell")
        airShell(team, teamTable, targetTeamTable, teamFlyingTable, targetTeamFlyingTable)
    elif parsedCommand[0] == "score": score()
    elif parsedCommand[0] == "turn": 
        for x in teamFlyingTable: kill(x)
        score()
        airPhase = False
    elif parsedCommand[0] == "details": details()
    elif parsedCommand[0] == "quit": quitGame()
    elif parsedCommand[0] == "help": helpText()
    elif parsedCommand[0] == "health": health(parsedCommand)
    elif parsedCommand[0] == "kill": kill(parsedCommand)
    elif parsedCommand[0] == "man": man(parsedCommand)
    elif parsedCommand[0] == "message": message()
    elif parsedCommand[0] == "info": info(parsedCommand)
    elif parsedCommand[0] == "use": use(parsedCommand)
    elif parsedCommand[0] == "dogfight": dogfight(parsedCommand, teamTable, targetTeamTable, teamFlyingTable, targetTeamFlyingTable)
    elif parsedCommand[0] == "survey": survey(parsedCommand, teamTable, teamFlyingTable)
    elif parsedCommand[0] == "bomb": bomb(parsedCommand, teamTable, targetTeamTable, teamFlyingTable)
    elif parsedCommand[0] == "missile": air_missile(parsedCommand, teamTable, targetTeamTable, teamFlyingTable)
    elif parsedCommand[0] == "use": use(parsedCommand)
    elif parsedCommand[0] == "survey": survey(parsedCommand, teamTable, teamFlyingTable)
    elif parsedCommand[0] == "takeoff": takeoff(parsedCommand)
    elif parsedCommand[0] == "land": land(parsedCommand)
    elif parsedCommand[0] == "pulse": pulse(parsedCommand, teamTable, targetTeamTable, teamFlyingTable)
    elif parsedCommand[0] == "airlift": airlift(parsedCommand, teamTable, teamFlyingTable)
    elif parsedCommand[0] == "kamikaze": kamikaze(parsedCommand, teamTable, targetTeamTable, teamFlyingTable)
    elif parsedCommand[0] == "save": save()
    else:
        error("command", "air-shell")
        airShell(team, teamTable, targetTeamTable, teamFlyingTable, targetTeamFlyingTable)
    commandNumber = commandNumber + 1
    log()
    if airPhase == True:
        airShell(team, teamTable, targetTeamTable, teamFlyingTable, targetTeamFlyingTable)

def shell(team, teamTable, targetTeamTable, teamFlyingTable, targetTeamFlyingTable):
    global airPhase
    global commandNumber
    if airPhase == True and airTheater == True:
        airShell(team, teamTable, targetTeamTable, teamFlyingTable, targetTeamFlyingTable)
        return
    prompt = str(round) + " ~ " + str(commandNumber) + " " + str(campaign) + ": " + str(team) + " % "
    rawCommand = input(prompt)
    parsedCommand = rawCommand.split()
    if fog() == True:
        print("This command fails.")
        commandNumber = commandNumber + 1
        return
    if not parsedCommand:
        error("command", "shell")
        return
    elif parsedCommand[0] == "score": score()
    elif parsedCommand[0] == "turn": turn()
    elif parsedCommand[0] == "details": details()
    elif parsedCommand[0] == "quit": quitGame()
    elif parsedCommand[0] == "help": helpText()
    elif parsedCommand[0] == "health": health(parsedCommand)
    elif parsedCommand[0] == "kill": kill(parsedCommand)
    elif parsedCommand[0] == "man": man(parsedCommand)
    elif parsedCommand[0] == "message": message()
    elif parsedCommand[0] == "freeze": freeze(parsedCommand)
    elif parsedCommand[0] == "convert": convert(parsedCommand, teamTable)
    elif parsedCommand[0] == "disable": disable(parsedCommand)
    elif parsedCommand[0] == "merge": merge(parsedCommand, teamTable)
    elif parsedCommand[0] == "split": split(parsedCommand, teamTable)
    elif parsedCommand[0] == "info": info(parsedCommand)
    elif parsedCommand[0] == "use": use(parsedCommand)
    elif parsedCommand[0] == "attack": attack(parsedCommand, teamTable, targetTeamTable)
    elif parsedCommand[0] == "move": move(parsedCommand, teamTable)
    elif parsedCommand[0] == "hide": hide(parsedCommand)
    elif parsedCommand[0] == "reveal": reveal(parsedCommand)
    elif parsedCommand[0] == "spy": spy(parsedCommand, teamTable)
    elif parsedCommand[0] == "fire": fire(parsedCommand, teamTable, targetTeamTable)
    elif parsedCommand[0] == "heading": heading(parsedCommand, teamTable)
    elif parsedCommand[0] == "torpedo": torpedo(parsedCommand, teamTable, targetTeamTable)
    elif parsedCommand[0] == "sortie": sortie(parsedCommand, teamTable, targetTeamTable)
    elif parsedCommand[0] == "depthcharge": depthcharge(parsedCommand, teamTable, targetTeamTable)
    elif parsedCommand[0] == "board": board(parsedCommand, teamTable, targetTeamTable)
    elif parsedCommand[0] == "build": build(parsedCommand, teamTable)
    elif parsedCommand[0] == "missile": missile(parsedCommand, teamTable, targetTeamTable)
    elif parsedCommand[0] == "nuke": nuke(parsedCommand, teamTable, targetTeamTable)
    elif parsedCommand[0] == "save": save()
    else:
        error("command", "shell")
        return
    commandNumber = commandNumber + 1
    log()

while True:
    while (round % 2) != 0: shell(firstTeam, firstTeamTable, secondTeamTable, firstTeamFlying, secondTeamFlying)
    while (round % 2) == 0: shell(secondTeam, secondTeamTable, firstTeamTable, secondTeamFlying, firstTeamFlying)