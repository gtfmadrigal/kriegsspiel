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
Umpire commands: score, turn, details, quit, help, health, kill, freeze, convert, disable, merge, split, info, use, man
Theater-agnostic commands: attack, move, hide, reveal, spy, fire
Naval commands: heading, torpedo, sortie, depthcharge, board
Army commands: build, missile
Air commands: takeoff, land, pulse, airlift, survey, bomb, kamikaze, dogfight, missile
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
convertTable = ["light-artillery", "med-artillery", "heavy-artillery", "light-cavalry", "med-cavalry", "heavy-cavalry"]
hideTable = ["infantry", "engineers", "mechanized", "light-artillery", "med-artillery", "heavy-artillery", "special", "attack-submarine", "missile-submarine", "stealth-bomber", "recon", "drone"]
hideableTerrain = ["forest", "swamp", "ocean", "air"]
airliftTable = ["infantry", "mechanized", "special", "light-cavalry"]

# Dictionaries
errorMessages = {"argument":"Bad argument for command. Type 'man [command] for details.", "team":"That unit belongs to the wrong team.", "available":"That unit is currently unavailable.", "function":"That function is unavailable to this unit.", "heading":"Unit cannot change heading more than 45 degrees without calling the heading command.", "dead":"Unit is dead.", "type":"No such unit type.", "unit":"No such unit.", "hidden":"Unit is already hidden.", "required":"Heading changes are not required for this unit.", "airborne":"Unit is not airborne.", "board":"Unit is not a boardable ship", "exists":"A unit with that name already exists.", "terrain":"The terrain does not allow for that function to be called.", "command":"Unknown command. Type 'help' to see a list of commands, or 'man [command]' to see how to use a particular command.", "type":"Wrong datatype passed to command."}
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
transportTable = {"transport":1}
kamikazeTable = {"light-fighter":6, "heavy-fighter":8}
moveFireTable = {"infantry":1, "engineers":1, "mechanized":1, "light-cavalry":1, "med-cavalry":1, "heavy-cavalry":1, "special":1, "corvette":1, "amphibious":1, "patrol":1, "cruiser":1, "destroyer":1, "battleship":1, "carrier":1, "light-fighter":1, "heavy-fighter":1, "bomber":1, "stealth-bomber":1, "recon":4, "transport":1, "drone":1}
bombTable = {"bomber":8, "stealth-bomber":6, "drone":10}
flyTable = {"light-fighter":1, "heavy-fighter":1, "bomber":1, "stealth-bomber":1, "recon":1, "transport":1, "drone":1}
structureTable = {}
manPages = {"score":"'score'", "turn":"'turn'", "details":"'details'", "quit":"'quit'", "help":"'help'", "health":"'health [unit]'", "kill":"'kill [unit]'", "convert":"'convert [unit]'", "disable":"'disable [unit]'", "merge":"'merge [unit1] [unit2] ... > [unit]'", "split":"'split [unit] > [unit1] [unit2] ...'", "info":"'info [unit]'", "use":"'use [unit]'", "man":"'man [command]'", "attack":"'attack [unit1] [unit2] ... > [unit3] [unit4] ...'", "hide":"'hide [unit]'", "reveal":"'reveal [unit]'", "fire":"'fire [unit1] [unit2] ... > [unit3] [unit4] ...'", "heading":"'heading [unit]'"}

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
    print("Origin:", str(function))

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

def reduce(unit):
    export = 0
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
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

def damage(unit, table): # DEBUGGED
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    if unit in immobileUnits or unit in usedUnits:
        error("available", "damage")
        return
    if unit in deadUnits:
        error("dead", "damage")
        return
    if not unitType in table: 
        error("function", "damage")
        return
    basicMaximum = table.get(unitType) + 1
    multiplier = dividedTable.get(unit, 1)
    maximum = basicMaximum * multiplier
    return random.randrange(1, maximum)

def fog():
    if fogOfWar == 1: return False
    export = random.randrange(1, fogOfWar + 1)
    if export == 1: return True
    else: return False

def kill(arguments):
    global firstTeamTable
    global secondTeamTable
    global firstTeamFlying
    global secondTeamTable
    unit = arguments[1]
    if unit in firstTeamTable: 
        table = firstTeamTable
        flyingTable = firstTeamFlying
    elif unit in secondTeamTable: 
        table = secondTeamTable
        flyingTable = secondTeamFlying
    else: 
        error("unit", "kill")
        return
    del table[unit]
    if unit in flyingTable: del flyingTable[unit]
    print(unit, "killed.")
    append(unit, deadUnits)
    update()

def dealDamage(units, damage, teamTable):
    global firstTeamTable
    global secondTeamTable
    for x in units:
        oldHealth = teamTable[x]
        if oldHealth - damage <= 0:
            kill(x)
        else:
            newHealth = oldHealth - damage
            teamTable[x] = newHealth
            print(x, "new health:", newHealth)
    update()

# Umpire commands
def score(): # DEBUGGED
    update()
    firstPercent = firstHealth / firstHealthTotal * 100
    secondPercent = secondHealth / secondHealthTotal * 100
    print(firstTeam, "total health:", firstHealth, "or", firstPercent, "%")
    print(secondTeam, "total health:", secondHealth, "or", secondPercent, "%")

def turn(): # DEBUGGED
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

def details(): # DEBUGGED
    print("Secrets:")
    print(secrets)
    print("Hidden units:")
    print(*hiddenUnits, sep = ", ")
    score()

def quitGame(): # DEBUGGED
    areYouSure = input("Are you sure you want to quit? [Yes/no]: ")
    if areYouSure == "yes" or areYouSure == "y":
        score()
        quit()

def helpText(): # DEBUGGED
    print("Commands: ")
    print(helpTextBlock)
    print("Unit types:")
    print(*allUnitTypes.keys(), sep = ", ")

def health(arguments): # DEBUGGED
    global firstTeamTable
    global secondTeamTable
    unit = arguments[1]
    try: newHealth = float(arguments[2])
    except:
        error("type", "health")
        return
    if unit in firstTeamTable: table = firstTeamTable
    elif unit in secondTeamTable: table = secondTeamTable
    else:
        error("unit", "health")
        return
    if newHealth <= 0: kill(arguments)
    else: table[unit] = float(newHealth)
    score()

def freeze(arguments):
    if len(arguments.split()) == 1: unit = arguments
    else: unit = arguments[1]
    append(unit, immobileUnits)

def use(arguments): # DEBUGGED
    if len(arguments) == 1: unit = str(arguments)
    else: unit = str(arguments[1])
    if unit in usedUnits: return
    append(unit, usedUnits)

def hide(arguments):
    global secrets
    global locationTable
    if len(arguments.split()) == 1: unit = arguments
    else: unit = arguments[1]
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    if not unitType in hideTable:
        error("function", "hide")
        return
    if unit in hiddenUnits:
        error("hidden", "hide")
        return
    structure = input("Structure to hide in, if any: ")
    if structure in structureTable:
        locationTable[unit] = structure
        append(unit, hiddenUnits)
        newSecret = unit + " hidden inside " + structure
        secrets = secrets + ", " + newSecret
        return
    terrain = input("Terrain to hide in: ")
    if not terrain in hideableTerrain:
        error("terrain", "hide")
        return
    append(unit, hiddenUnits)
    locationTable[unit] = terrain
    location = input("Location of this hidden unit: ")
    newSecret = unit + " hidden at " + location
    secrets = secrets + ", " + newSecret

def reveal(arguments):
    global secrets
    global locationTable
    if len(arguments.split()) == 1: unit = arguments
    else: unit = arguments[1]
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    if not unit in hiddenUnits or not unitType in hideTable:
        error("function", "reveal")
        return
    newLocation = input("New terrain: ")
    locationTable[unit] = newLocation
    remove(unit, hiddenUnits)
    newSecret = unit + " is no longer hidden."
    secrets = secrets + ", " + newSecret

def convert(arguments, teamTable):
    global firstTeamTable
    global secondTeamTable
    global unitTable
    unit = arguments[1]
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    if not unit in teamTable:
        error("team", "convert")
        return
    if not unitType in convertTable:
        error("function", "convert")
        return
    currentHealth = teamTable.get(unit)
    unitTable[unit] = "infantry"
    if currentHealth > 4: newHealth = 4
    else: newHealth = currentHealth
    teamTable[unit] = newHealth
    update()

def disable(arguments):
    if len(arguments.split()) == 1: unit = arguments
    else: unit = arguments[1]
    freeze(unit)
    use(unit)
    append(unit, disabledUnits)

def merge(arguments, teamTable):
    global firstTeamTable
    global secondTeamTable
    global unitTable
    global dividedTable
    del arguments[0]
    mergedLocalUnitType = unitTable.get(arguments[0])
    mergedUnitType = allUnitTypes.get(mergedLocalUnitType)
    totalHealth = 0
    numberOfUnits = 0
    mergedUnits = []
    finalUnit = ""
    immobile = False
    disabled = False
    used = False
    hidden = False
    for x in arguments:
        if x in teamTable:
            if unitTable[x] == mergedUnitType:
                numberOfUnits = numberOfUnits + 1
                totalHealth = totalHealth + teamTable[x]
                mergedUnits.append(x)
                if x in immobileUnits: immobile = True
                if x in disabledUnits: disabled = True
                if x in usedUnits: used = True
                if x in hiddenUnits: hidden = True
            else:
                print(x, "could not be merged.")
        elif x == ">": pass
        else:
            if x in unitTable:
                error("exists", "merge")
                return
            finalUnit = x
            break
    teamTable[finalUnit] = totalHealth
    unitTable[finalUnit] = mergedUnitType
    dividedTable[finalUnit] = numberOfUnits
    for x in mergedUnits: 
        del teamTable[x]
        del unitTable[x]
    if immobile == True: freeze(finalUnit)
    if used == True: use(finalUnit)
    if disabled == True: disable(finalUnit)
    if hidden == True: hide(finalUnit)

def split(arguments, teamTable):
    global firstTeamTable
    global secondTeamTable
    global dividedTable
    global unitTable
    del arguments[0]
    originalUnit = arguments[0]
    localUnitType = unitTable.get(originalUnit)
    unitType = allUnitTypes.get(localUnitType)
    numberOfUnits = 0
    newUnits = []
    currentHealth = teamTable.get(originalUnit)
    if not originalUnit in dividedTable or not unitType in splitTable:
        error("function", "split")
        return
    for x in arguments:
        if x in teamTable: pass
        elif x == ">": pass
        else:
            if x in unitTable:
                print(x, "could not be created.")
            else:
                numberOfUnits = numberOfUnits + 1
                newUnits.append(x)
    newHealth = currentHealth / numberOfUnits
    for x in newUnits:
        teamTable[x] = newHealth
        unitTable[x] = unitType
        if originalUnit in immobileUnits: freeze(x)
        if originalUnit in disabledUnits: disable(x)
        if originalUnit in usedUnits: use(x)
        if originalUnit in hiddenUnits: hide(x)
        dividedTable[x] = 1 / numberOfUnits
    del teamTable[originalUnit]
    del unitTable[originalUnit]
    if originalUnit in dividedTable: del dividedTable[originalUnit] 
    if originalUnit in immobileUnits: remove(originalUnit, immobileUnits)
    if originalUnit in disabledUnits: 
        remove(originalUnit, disabledUnits)
        reveal(originalUnit)
    if originalUnit in usedUnits: remove(originalUnit, usedUnits)
    if originalUnit in hiddenUnits: reveal(originalUnit)       

def man(arguments): # DEBUGGED
    command = arguments[1]
    if not str(command) in manPages:
        error("command", "man")
        print("Type 'help' for a list of commands.")
        return
    print(manPages.get(command))

# Theater-agnostic functions
def attack(arguments, teamTable, targetTeamTable):
    totalAttackDamage = 0
    totalDefenseDamage = 0
    defendingUnits = []
    del arguments[0]
    for x in arguments:
        if x == ">": pass
        elif x in teamTable:
            if x in usedUnits: continue
            initialDamage = damage(x, attackTable)
            if initialDamage == None: continue
            if type(reduce(x)) == None: pass
            else: finalDamage = initialDamage - reduce(x)
            totalAttackDamage = totalAttackDamage + finalDamage
            if x in hiddenUnits: reveal(x)
            use(x)
            if not x in moveFireTable: freeze(x)
        elif x in targetTeamTable:
            initialDefense = damage(x, attackTable)
            if initialDefense == None: continue
            totalDefenseDamage = totalDefenseDamage + initialDefense
            defendingUnits.append(x)
            if x in hiddenUnits: reveal(x)
            use(x)
            if not x in moveFireTable: freeze(x)
        else: print(x, " does not exist.")
    if totalDefenseDamage >= totalAttackDamage:
        print("Attack repelled.")
        return
    netDamage = totalAttackDamage - totalDefenseDamage
    print("Net damage: ", netDamage)
    perUnitDamage = netDamage / len(defendingUnits.split())
    print("Damage per unit:", perUnitDamage)
    for x in defendingUnits:
        location = locationTable.get(x)
        if location in structureTable:
            reducedDamage = fortificationReduce(location, perUnitDamage)
        else: reducedDamage = perUnitDamage
        dealDamage(defendingUnits, reducedDamage, targetTeamTable)
    defendingUnits.clear()
    score()
    turn()

def move(arguments, teamTable):
    global locationTable
    unit = arguments[1]
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    if not unit in teamTable:
        error("team", "convert")
        return
    if unit in immobileUnits:
        error("available", "move")
        return
    if unitType in headingTable:
        error("heading", "move")
    if not unitType in moveFireTable:
        use(unit)
    currentLocation = locationTable.get(unit)
    print("Current location or terrain: ", currentLocation)
    newLocation = input("New location or terrain: ")
    if unit in hiddenUnits:
        if not newLocation in structureTable or not newLocation in hideableTerrain:
            reveal(unit)
    locationTable[unit] = str(newLocation)
    freeze(unit)

def spy(arguments, teamTable):
    unit = arguments[1]
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
    if effectiveness >= 6: print("Good information.")
    elif effectiveness == 1: print("Bad information.")
    else: print("No information.")
    details()
    use(unit)

def fire(arguments, teamTable, targetTeamTable):
    del arguments[0]
    totalAttackDamage = 0
    defendingUnits = []
    for x in arguments:
        if x == ">": pass
        elif x in teamTable:
            if x in usedUnits: continue
            initialDamage = damage(x, fireTable)
            if initialDamage == None: continue
            totalAttackDamage = initialDamage + totalAttackDamage
            use(x)
            if not x in moveFireTable: freeze(x)
            if x in hiddenUnits: reveal(x)
        elif x in targetTeamTable:
            defendingUnits.append(x)
        else: print(x, " does not exist.")
    print("Damage:", totalAttackDamage)
    perUnitDamage = totalAttackDamage / len(defendingUnits.split())
    print("Damage per unit:", perUnitDamage)
    for x in defendingUnits:
        location = locationTable.get(x)
        if location in structureTable:
            reducedDamage = fortificationReduce(location, perUnitDamage)
        else: reducedDamage = perUnitDamage
        dealDamage(defendingUnits, reducedDamage, targetTeamTable)
    defendingUnits.clear()
    score()

# Naval functions
def heading(arguments, teamTable):
    unit = arguments[1]
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
    freeze(unit)
    if not unitType in moveFireTable: use(unit)

def torpedo(arguments, teamTable, targetTeamTable):
    del arguments[0]
    unit = arguments[0]
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    if unit in immobileUnits or unit in usedUnits:
        error("available", "torpedo")
        return
    if not unitType in torpedoTable:
        error("function", "torpedo")
        return
    effectiveness = 0
    for x in arguments:
        if x == ">": pass
        elif x in teamTable: effectiveness = damage(x, torpedoTable)
        elif x in targetTeamTable: target = x
        else: print(x, "does not exist.")
    oldHealth = targetTeamTable.get(target)
    if effectiveness == 6 or oldHealth - effectiveness <= 0:   
        kill(target)
    else:
        newHealth = oldHealth - effectiveness
        targetTeamTable[target] = newHealth
    use(unit)
    freeze(unit)
    if unit in hiddenUnits: reveal(unit)
    score()

def sortie(arguments, teamTable, targetTeamTable):
    del arguments[0]
    unit = arguments[0]
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
        if x == ">": pass
        elif x in teamTable: attackDamage = damage(x, sortieTable)
        elif x in targetTeamTable: 
            defenseDamage = damage(x, sortieDefenseTable)
            defendingUnits.append(x)
        else: print(x, "does not exist.")
    if defenseDamage >= attackDamage: print("Sortie repelled.")
    else:
        netDamage = attackDamage - defenseDamage
        perUnitDamage = netDamage / len(defendingUnits.split())
        for x in defendingUnits:
            if x in hiddenUnits: reveal(x)
            dealDamage(defendingUnits, perUnitDamage, targetTeamTable)
    use(unit)
    score()

def depthcharge(arguments, teamTable, targetTeamTable):
    global firstTeamTable
    global secondTeamTable
    del arguments[0]
    unit = arguments [0]
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    if unit in alreadyDropped:
        error("available", "depthcharge")
        return
    if not unitType in depthchargeTable:
        error("function", "depthcharge")
        return
    for x in arguments:
        if x == ">": pass
        elif x in teamTable: effectiveness = damage(x, depthchargeTable)
        elif x in targetTeamTable: target = x
        else: print(x, "does not exist.")
    if effectiveness == 6: kill(target)
    elif effectiveness == 5:
        print(target, "disabled.")
        disable(target)
    else: print("Missed.")
    freeze(unit)
    append(unit, alreadyDropped)
    score()

def board(arguments, teamTable, targetTeamTable):
    global firstTeamTable
    global secondTeamTable
    del arguments[0]
    unit = arguments[0]
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
        if x == ">": pass
        elif x in teamTable: effectiveness = damage(x, boardTable)
        elif x in targetTeamTable: target = x
        else: print(x, "does not exist.")
    if effectiveness >= 5:
        print(target, "seized.")
        targetHealth = targetTeamTable.get(target)
        del targetTeamTable[target]
        teamTable[target] = targetHealth
        freeze(unit)
    else:
        print("Seizure failed.")
        print(unit, "suffers", str(effectiveness), "damage.")
        if currentHealth - effectiveness <= 0:
            kill(unit)
        else:
            newHealth = currentHealth - effectiveness
            teamTable[unit] = newHealth
        disable(unit)
    use(unit)
    score()

# Army functions
def build(arguments, teamTable):
    global structureTable
    unit = arguments[1]
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
    use(unit)
    if not unitType in moveFireTable: freeze(unit)

def missile(arguments, teamTable, targetTeamTable):
    global firstTeamTable
    global secondTeamTable
    del arguments[0]
    for x in arguments:
        if x == ">": pass
        elif x in teamTable: 
            unit = x
            if x in hiddenUnits: reveal(x)
            use(x)
        elif x in targetTeamTable: target = x
        else: print(x, "does not exist.")
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
        else: netDamage = attackDamage - defenseDamage
    else: netDamage = attackDamage
    if targetLocation in structureTable:
        finalDamage = fortificationReduce(targetLocation, netDamage)
    else: finalDamage = netDamage
    dealDamage(target, finalDamage, targetTeamTable)
    use(unit)
    score()

# Air functions
def takeoff(arguments): # DEBUGGED
    unit = arguments[1]
    if unit in firstTeamTable: teamFlyingTable = firstTeamFlying
    elif unit in secondTeamTable: teamFlyingTable = secondTeamFlying
    else:
        error("unit", "takeoff")
        return
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    if not unitType in flyTable:
        error("function", "takeoff")
        return
    if unit in teamFlyingTable:
        print("Already airborne.")
        return
    append(unit, teamFlyingTable)
    if unitType in hideTable:
        hide(unit)

def land(arguments):
    unit = arguments[1]
    if unit in firstTeamTable: teamFlyingTable = firstTeamFlying
    elif unit in secondTeamTable: teamFlyingTable = secondTeamFlying
    else:
        error("unit", "takeoff")
        return
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    if not unitType in flyTable:
        error("function", "takeoff")
        return
    if not unit in teamFlyingTable:
        error("airborne", "takeoff")
        return
    remove(unit, teamFlyingTable)
    use(unit)

def pulse(arguments, teamTable, targetTeamTable, teamFlyingTable):
    del arguments[0]
    defendingUnits = []
    for x in arguments:
        if x == ">": pass
        elif x in teamTable:
            if x in teamFlyingTable:
                unit = x
            else: print(x, "is not airborne.")
        elif x in targetTeamTable:
            defendingUnits.append(x)
        else: print(x, "does not exist.")
    localUnitType = unitTable.get(unit)
    unitType = allUnitTypes.get(localUnitType)
    if unitType in usedUnits:
        error("available", "pulse")
        return
    if not unitType in pulseTable:
        error("function", "pulse")
        return
    effectiveness = damage(unit, pulseTable)
    if effectiveness == 6:
        print("Pulse effective.")
        for x in defendingUnits: disable(x)
    else:
        print("Pulse ineffective.")
    use(unit)

def airlift(arguments, teamTable, teamFlyingTable):
    global locationTable
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
                if liftedUnitType in airliftTable:
                    liftedUnits.append(x)
                else:
                    print(x, "cannot be airlifted.")
        else: print(x, "does not exist, or does not belong to you.")
    localUnitType = unitTable.get(x)
    unitType = allUnitTypes.get(localUnitType)
    if unit in usedUnits:
        error("availahle", "pulse")
        return
    if not unitType in transportTable:
        error("function", "pulse")
        return
    for x in liftedUnits:
        currentLocation = locationTable.get(x)
        print("Current location or terrain: ", currentLocation)
        newLocation = input("New location or terrain: ")
        if x in hiddenUnits:
            if not newLocation in structureTable or not newLocation in hideableTerrain:
                reveal(x)
        locationTable[x] = str(newLocation)
    use(unit)

def kamikaze(arguments, teamTable, targetTeamTable, teamFlyingTable):
    del arguments[0]
    for x in arguments:
        if x == ">": pass
        elif x in teamTable:
            if not x in teamFlyingTable:
                error("airborne", "kamikaze")
                return
            else:
                unit = x
        elif x in targetTeamTable: target = x
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
    if effectiveness == 6: kill(target)
    else: dealDamage(target, effectiveness, targetTeamTable)
    kill(unit)
    score()

def air_missile(arguments, teamTable, targetTeamTable, teamFlyingTable):
    global firstTeamTable
    global secondTeamTable
    del arguments[0]
    for x in arguments:
        if x == ">": pass
        elif x in teamTable:
            if not x in teamFlyingTable:
                error("airborne", "air-missile")
                return
            unit = x
            if x in hiddenUnits: reveal(x)
            use(x)
        elif x in targetTeamTable: target = x
        else: print(x, "does not exist.")
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
        else: netDamage = attackDamage - defenseDamage
    else: netDamage = attackDamage
    if targetLocation in structureTable:
        finalDamage = fortificationReduce(targetLocation, netDamage)
    else: finalDamage = netDamage
    dealDamage(target, finalDamage, targetTeamTable)
    use(unit)
    score()

def dogfight(arguments, teamTable, targetTeamTable, teamFlyingTable, targetTeamFlyingTable): # DEBUGGED
    totalAttackDamage = 0
    totalDefenseDamage = 0
    defendingUnits = []
    del arguments[0]
    for x in arguments:
        if x == ">": pass
        elif x in teamTable:
            if not x in teamFlyingTable:
                print(x, "is not airborne.")
                continue
            if x in usedUnits: continue
            initialDamage = damage(x, attackTable)
            if initialDamage == None: continue
            if reduce(x) == None: finalDamage = initialDamage
            else: finalDamage = initialDamage - reduce(x)
            totalAttackDamage = totalAttackDamage + finalDamage
            if x in hiddenUnits: reveal(x)
            use(x)
            if not x in moveFireTable: freeze(x)
        elif x in targetTeamTable:
            if not x in targetTeamFlyingTable:
                print(x, "is not airborne.")
                continue
            initialDefense = damage(x, attackTable)
            if initialDefense == None: continue
            totalDefenseDamage = totalDefenseDamage + initialDefense
            defendingUnits.append(x)
            if x in hiddenUnits: reveal(x)
            use(x)
            if not x in moveFireTable: freeze(x)
        else: print(x, " does not exist.")
    print(totalAttackDamage)
    print(totalDefenseDamage)
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
    score()
    turn()

def bomb(arguments, teamTable, targetTeamTable, teamFlyingTable):
    del arguments[0]
    totalAttackDamage = 0
    defendingUnits = []
    for x in arguments:
        if x == ">": pass
        elif x in teamTable:
            if not x in teamFlyingTable:
                error("airborne")
                return
            if x in usedUnits: continue
            initialDamage = damage(x, fireTable)
            if initialDamage == None: continue
            totalAttackDamage = initialDamage + totalAttackDamage
            use(x)
            if not x in moveFireTable: freeze(x)
            if x in hiddenUnits: reveal(x)
        elif x in targetTeamTable:
            defendingUnits.append(x)
        else: print(x, " does not exist.")
    print("Damage:", totalAttackDamage)
    perUnitDamage = totalAttackDamage / len(defendingUnits.split())
    print("Damage per unit:", perUnitDamage)
    for x in defendingUnits:
        location = locationTable.get(x)
        if location in structureTable:
            reducedDamage = fortificationReduce(location, perUnitDamage)
        else: reducedDamage = perUnitDamage
        dealDamage(defendingUnits, reducedDamage, targetTeamTable)
    defendingUnits.clear()
    score()

def survey(arguments, teamTable, teamFlyingTable):
    unit = arguments[1]
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
    if effectiveness >= 6: print("Good information.")
    elif effectiveness == 1: print("Bad information.")
    else: print("No information.")
    details()
    use(unit)

# Shell functions
def info(arguments): # DEBUGGED
    unit = arguments[1]
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
    healthPercentage = teamTable.get(unit) / healthTable.get(unitType)
    print("Health percentage:", healthPercentage)
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
    if unitType in transportTable: print("Can transport other units.")
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
    if parsedCommand[0] == "score": score()
    elif parsedCommand[0] == "turn": 
        score()
        airPhase = False
    elif parsedCommand[0] == "details": details()
    elif parsedCommand[0] == "quit": quitGame()
    elif parsedCommand[0] == "help": helpText()
    elif parsedCommand[0] == "health": health(parsedCommand)
    elif parsedCommand[0] == "kill": kill(parsedCommand)
    elif parsedCommand[0] == "man": man(parsedCommand)
    elif parsedCommand[0] == "info": info(parsedCommand)
    elif parsedCommand[0] == "use": use(parsedCommand)
    elif parsedCommand[0] == "dogfight": dogfight(parsedCommand, teamTable, targetTeamTable, teamFlyingTable, targetTeamFlyingTable)
    elif parsedCommand[0] == "survey": survey(parsedCommand, teamTable, teamFlyingTable)
    elif parsedCommand[0] == "bomb": bomb(parsedCommand, teamTable, targetTeamTable, teamFlyingTable)
    elif parsedCommand[0] == "heading": heading(parsedCommand)
    elif parsedCommand[0] == "missile": air_missile(parsedCommand, teamTable, targetTeamTable, teamFlyingTable)
    elif parsedCommand[0] == "use": use(parsedCommand)
    elif parsedCommand[0] == "attack": attack(parsedCommand, teamTable, targetTeamTable)
    elif parsedCommand[0] == "move": move(parsedCommand)
    elif parsedCommand[0] == "hide": hide(parsedCommand)
    elif parsedCommand[0] == "reveal": reveal(parsedCommand)
    elif parsedCommand[0] == "spy": spy(parsedCommand)
    elif parsedCommand[0] == "fire": fire(parsedCommand, teamTable, targetTeamTable)
    elif parsedCommand[0] == "heading": heading(parsedCommand)
    elif parsedCommand[0] == "torpedo": torpedo(parsedCommand, teamTable, targetTeamTable)
    elif parsedCommand[0] == "sortie": sortie(parsedCommand, teamTable, targetTeamTable)
    elif parsedCommand[0] == "depthcharge": depthcharge(parsedCommand, teamTable, targetTeamTable)
    elif parsedCommand[0] == "board": board(parsedCommand, teamTable, targetTeamTable)
    elif parsedCommand[0] == "build": build(parsedCommand)
    elif parsedCommand[0] == "takeoff": takeoff(parsedCommand)
    elif parsedCommand[0] == "land": land(parsedCommand)
    elif parsedCommand[0] == "pulse": pulse(parsedCommand, teamTable, targetTeamTable, teamFlyingTable)
    elif parsedCommand[0] == "airlift": airlift(parsedCommand, teamTable, teamFlyingTable)
    elif parsedCommand[0] == "kamikaze": kamikaze(parsedCommand, teamTable, targetTeamTable, teamFlyingTable)
    else:
        error("command", "air-shell")
        airShell(team, teamTable, targetTeamTable, teamFlyingTable, targetTeamFlyingTable)
    commandNumber = commandNumber + 1
    if airPhase == True:
        airShell(team, teamTable, targetTeamTable, teamFlyingTable, targetTeamFlyingTable)

def shell(team, teamTable, targetTeamTable, teamFlyingTable, targetTeamFlyingTable):
    global airPhase
    global commandNumber
    if airPhase == True and airTheater == True:
        airShell(team, teamTable, targetTeamTable, teamFlyingTable, targetTeamFlyingTable)
        return
    for x in teamFlyingTable:
        land(x)
        kill(x)
    prompt = str(round) + " ~ " + str(commandNumber) + " " + str(campaign) + ": " + str(team) + " % "
    rawCommand = input(prompt)
    parsedCommand = rawCommand.split()
    if fog() == True:
        print("This command fails.")
        commandNumber = commandNumber + 1
        return
    if parsedCommand[0] == "score": score()
    elif parsedCommand[0] == "turn": turn()
    elif parsedCommand[0] == "details": details()
    elif parsedCommand[0] == "quit": quitGame()
    elif parsedCommand[0] == "help": helpText()
    elif parsedCommand[0] == "health": health(parsedCommand)
    elif parsedCommand[0] == "kill": kill(parsedCommand)
    elif parsedCommand[0] == "man": man(parsedCommand)
    elif parsedCommand[0] == "freeze": freeze(parsedCommand)
    elif parsedCommand[0] == "convert": convert(parsedCommand, teamTable)
    elif parsedCommand[0] == "disable": disable(parsedCommand)
    elif parsedCommand[0] == "merge": merge(parsedCommand, teamTable)
    elif parsedCommand[0] == "split": split(parsedCommand, teamTable)
    elif parsedCommand[0] == "info": info(parsedCommand)
    elif parsedCommand[0] == "use": use(parsedCommand)
    elif parsedCommand[0] == "attack": attack(parsedCommand, teamTable, targetTeamTable)
    elif parsedCommand[0] == "move": move(parsedCommand)
    elif parsedCommand[0] == "hide": hide(parsedCommand)
    elif parsedCommand[0] == "reveal": reveal(parsedCommand)
    elif parsedCommand[0] == "spy": spy(parsedCommand)
    elif parsedCommand[0] == "fire": fire(parsedCommand, teamTable, targetTeamTable)
    elif parsedCommand[0] == "heading": heading(parsedCommand)
    elif parsedCommand[0] == "torpedo": torpedo(parsedCommand, teamTable, targetTeamTable)
    elif parsedCommand[0] == "sortie": sortie(parsedCommand, teamTable, targetTeamTable)
    elif parsedCommand[0] == "depthcharge": depthcharge(parsedCommand, teamTable, targetTeamTable)
    elif parsedCommand[0] == "board": board(parsedCommand, teamTable, targetTeamTable)
    elif parsedCommand[0] == "build": build(parsedCommand)
    elif parsedCommand[0] == "missile": missile(parsedCommand, teamTable, targetTeamTable)
    else:
        error("command", "shell")
        return
    commandNumber = commandNumber + 1

while True:
    while (round % 2) != 0: shell(firstTeam, firstTeamTable, secondTeamTable, firstTeamFlying, secondTeamFlying)
    while (round % 2) == 0: shell(secondTeam, secondTeamTable, firstTeamTable, secondTeamFlying, firstTeamFlying)