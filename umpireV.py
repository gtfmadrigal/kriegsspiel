import random
import sys

# set strings
round = 1
commandNumber = 1

# import data from gamefile

# create lists
hiddenUnits = []
hideTable = ["lightInfantry", "mediumInfantry", "heavyInfantry", "special", "engineer", "spy", "command", "lightArtillery", "mediumArtillery", "heavyArtillery", "attackSubmarine", "missileSubmarine", "stealthBomber", "recon", "transport", "drone"]
hideableTerrain = ["forest", "jungle", "swamp", "mountain"]
secrets = []
usedUnits = []
deadUnits = []
immobileUnits = []
allUnits = []
headingTable = ["corvette", "destroyer", "carrier", "battleship", "cruiser"]

# create dictionaries
attackTable = {"lightInfantry":4, "mediumInfantry":4, "heavyInfantry":6, "special":12, "engineer":4, "spy":4, "command":12, "lightArtillery":4, "mediumArtillery":4, "heavyArtillery":4, "lightCavalry":6, "mediumCavalry":8, "heavyCavalry":10, "amphibious":4, "patrol":4, "corvette":6, "destroyer":8, "carrier":12, "battleship":12, "cruiser":12, "heavyFighter":6, "attackSubmarine":0, "missileSubmarine":0, "lightFighter":4, "bomber":4, "stealthBomber":4, "transport":4, "recon":4, "drone":4}
movementTable = {"foot": 1.5, "horse": 12, "motor": 25, "tank": 15, "oar": 2, "sail": 3, "steam": 10, "nuclear": 20}
terrainSpeedTable = {"unpaved":1, "paved":2, "forest":-1, "hills":-1, "creek":-2, "denseForest":-2, "steepHills":-2, "swamp":-3, "jungle":-3, "mountains":-3, "plains":0}

# create effect dictionaries from gamefile
strengthTable = {}
speedTable = {}
precisionTable = {}
hasteTable = {}
industryTable = {}
regenerationTable = {}
resistanceTable = {}
nobilityTable = {}
visionTable = {}
silenceTable = {}
wisdomTable = {}
gallantryTable = {}

# Initialization
from foo import *
for x in hideableLocations: hideableTerrain.append(x)
for x in permanentlyImmobileUnits: immobileUnits.append(x)
for x in firstTeamTable: allUnits.append(x)
for x in secondTeamTable: allUnits.append(x)
for x in allUnits:
    strengthTable[x] = 0
    unitType = unitTable.get(x)
    if unitType == "special": speedTable[x] = 1
    elif unitType == "engineers": speedTable[x] = -1
    elif unitType == "lightArtillery": speedTable[x] = -1
    elif unitType == "mediumCavalry": speedTable[x] = -2
    elif unitType == "heavyInfantry": speedTable[x] = -2
    elif unitType == "mediumArtillery": speedTable[x] = -2
    elif unitType == "carrier": speedTable[x] = -2
    elif unitType == "heavyCavalry": speedTable[x] = -3
    elif unitType == "heavyArtillery": speedTable[x] = -3
    else: speedTable[x] = 0
    precisionTable[x] = 0
    hasteTable[x] = 0
    industryTable[x] = 0
    regenerationTable[x] = 0
    resistanceTable[x] = 0
    nobilityTable[x] = 0
    visionTable[x] = 0
    silenceTable[x] = 0
    wisdomTable[x] = 0
    gallantryTable[x] = 0

# Meta-functions

def critical(attack, defense):
    global strengthTable
    global resistanceTable
    global gallantryTable
    modifier = gallantryTable.get(defense)
    base = random.randrange(1, 6)
    result = base + modifier
    if result <= 1:
        kill(defense)
        attackingStrength = strengthTable.get(attack)
        strengthTable[attack] = attackingStrength - 2
    if result == 2:
        print(defense, " is moved 0.5*max away from the battle.")
        move(defense)
        effect(defense, strengthTable, -4)
        effect(defense, resistanceTable, -4)
        effect(defense, gallantryTable, -4)
        effect(attack, strengthTable, -1)
    if result == 3:
        effect(defense, strengthTable, -3)
        effect(defense, resistanceTable, -3)
        effect(defense, gallantryTable, -3)
    if result == 4:
        effect(defense, strengthTable, -2)
        effect(defense, resistanceTable, -2)
        effect(defense, gallantryTable, -2)
    if result == 5:
        effect(defense, strengthTable, -1)
        effect(defense, resistanceTable, -1)
        effect(defense, gallantryTable, -1)
        effect(attack, strengthTable, 1)
        effect(attack, resistanceTable, 1)
        effect(attack, gallantryTable, 1)
    if result >= 6:
        effect(defense, strengthTable, 4)
        effect(defense, resistanceTable, -1)
        effect(defense, gallantryTable, -3)
        effect(attack, strengthTable, 2)
        effect(attack, resistanceTable, 2)
        effect(attack, gallantryTable, 2)

def kill(arguments):
    global firstTeamTable
    global secondTeamTable
    global deadUnits
    unit = arguments[0]
    if unit in firstTeamTable: firstTeamTable.remove(unit)
    if unit in secondTeamTable: secondTeamTable.remove(unit)
    deadUnits.append(unit)

def structureDamage(damage, location):
    global structureStrengthTable
    global terrainTable
    global hiddenUnits
    oldStructureHealth = structureStrengthTable(location)
    newStructureHealth = oldStructureHealth - damage
    if newStructureHealth > 0:
        structureStrengthTable[location] = newStructureHealth
        print(location, " has health: ", newStructureHealth)
        return 0
    print(location, " has been destroyed.")
    affectedUnits = [k for k, unit in terrainTable if unit == location]
    newLocation = input("New location for units in destroyed structure: ")
    for x in affectedUnits:
        reveal(x)
        terrainTable[x] = newLocation
    terrainTable.remove[location]
    adjustedDamage = damage - oldStructureHealth
    return adjustedDamage

def damage(unit, damage, teamTable):
    global firstTeamTable
    global secondTeamTable
    oldHealth = teamTable.get(unit)
    location = terrainTable.get(unit)
    if location in structureStrengthTable: newDamage = structureDamage(damage, location)
    else: newDamage = damage
    if oldHealth - newDamage <= 0: kill(unit)
    else:
        newHealth = oldHealth - damage
        teamTable[unit] = newHealth
        print(unit, " has health: ", newHealth)

def effect(unit, effectTable, amount):
    global strengthTable
    global speedTable
    global precisionTable
    global hasteTable
    global industryTable
    global regenerationTable 
    global resistanceTable
    global nobilityTable
    global visionTable
    global silenceTable
    global wisdomTable
    global gallantryTable
    oldUnitEffect = effectTable.get(unit)
    newUnitEffect = oldUnitEffect + amount
    effectTable[unit] = newUnitEffect

# Umpire commands

def hide(arguments):
    global secrets
    global hiddenUnits
    if len(arguments) == 1: unit = arguments
    else: unit = arguments[1]
    try: unitType = unitTable.get(unit)
    except:
        print("Error parsing arguments in command hide().")
        return
    silence = silenceTable.get(unit)
    if silence <= -2:
        print(unit, " cannot hide, as its silence level is: ", silence)
        return
    if not unitType in hideTable:
        print(unit, " cannot hide, as its type is: ", unitType)
        return
    try: terrain = terrainTable.get(unit)
    except: terrain = "plains"
    if not terrain in hideableTerrain:
        print(unit, " cannot hide, as its location is: ", terrain)
    if unit in hiddenUnits:
        print(unit, "is already hidden at location: ", terrain)
    newSecret = unit + " is hidden at: " + terrain
    secrets.append(newSecret)
    hiddenUnits.append(unit)

def reveal(arguments):
    global hiddenUnits
    if len(arguments) == 1: unit = arguments
    else: unit = arguments[1]
    if not unit in hiddenUnits:
        print(unit, " is not hidden.")
        return
    hiddenUnits.remove[unit]
    print("Display ", unit, " on the board.")

# Theater-agnostic commands
    
def attack(arguments, teamTable, targetTeamTable):
    global hiddenUnits
    global usedUnits
    global silenceTable
    global immobileUnits
    attackingUnits = []
    defendingUnits = []
    totalAttack = 0
    totalDefense = 0
    attackCritical = 0
    defenseCritical = 0
    # deal damage
    # reveal
    del arguments[0]
    for x in arguments:
        if x == ">": pass
        elif x in usedUnits: pass
        elif x in teamTable: 
            attackingUnits.append(x)
            if x in hiddenUnits: reveal(x)
        elif x in targetTeamTable: defendingUnits.append(x)
        else: print(x, " does not exist.")
    for x in attackingUnits:
        unitType = unitTable.get[x]
        max = attackTable.get[unitType]
        strength = strengthTable.get[x]
        base = random.randrange(1, max)
        total = base + strength
        if total >= max: attackCritical = True
        totalAttack = totalAttack + total
        if unitTable[x] == "lightInfantry": effect(x, silenceTable, -1)
        if unitTable[x] == "special": effect(x, silenceTable, -1)
        else: effect(x, silenceTable, -2)
        reveal(x)
        immobileUnits.append(x)
    for x in defendingUnits:
        unitType = unitTable.get[x]
        max = attackTable.get[unitType]
        resistance = resistanceTable.get[x]
        base = random.randrange(1, max)
        total = base + resistance
        if total <= 1: 
            total = 1
            defenseCritical = True
        totalDefense = totalDefense + total
        if unitTable[x] == "lightInfantry": effect(x, silenceTable, -1)
        if unitTable[x] == "special": effect(x, silenceTable, -1)
        else: effect(x, silenceTable, -2)
        reveal(x)
        immobileUnits.append(x)
    if totalDefense >= totalAttack:
        print("Attack repelled.")
        return
    netDamage = totalAttack - totalDefense
    if attackCritical > 0 and defenseCritical > 0:
        criticalUnits = min(attackCritical, defenseCritical)
        while criticalUnits > 0:
            attackCriticalUnit = (random.choice(attackingUnits))
            defenseCriticalUnit = (random.choice(defendingUnits))
            critical(attackCriticalUnit, defenseCriticalUnit)
            criticalUnits - 1
    perUnitDamage = netDamage / len(defendingUnits)
    for x in defendingUnits: damage(x, perUnitDamage, targetTeamTable)

def move(arguments, teamTable):
    global terrainTable
    global usedUnits
    movingUnits = []
    for x in arguments:
        if x == ">": pass
        if x in teamTable: movingUnits.append(x)
        if x in terrainTable: destination = x
        else: print(x, " is not a unit or location.")
    try: terrainSpeedTable.get(destination)
    except: destination = "plains"
    for x in movingUnits:
        if x in immobileUnits:
            print(x, " is immobile.")
            pass
        unitType = unitTable.get(x)
        if unitType in headingTable:
            print(x, "cannot move without changing heading.")
            pass
        movementType = unitMovementType.get(unitType)
        baseMovement = movementTable.get(movementType)
        oldSpeed = speedTable.get(x)
        try: oldLocation = terrainTable.get(x)
        except: oldLocation = "plains"
        oldLocationSpeed = terrainSpeedTable.get(oldLocation)
        speedAdjustment = oldSpeed - oldLocationSpeed
        distanceModifier = 1 + (0.3 * oldSpeed)
        distance = baseMovement * distanceModifier
        print(x, " can move: ", distance, " units.")
        terrainTable.remove(x)
        speedTable.remove(x)
        terrainTable[x] = destination
        destinationSpeed = terrainSpeedTable.get(destination)
        destinationSpeedAdjusted = destinationSpeed + speedAdjustment
        speedTable[x] = destinationSpeedAdjusted

def disengage(arguments):
    global immobileUnits
    global speedTable
    global gallantryTable
    unit = arguments[0]
    if unit in permanentlyImmobileUnits:
        print(unit, " is permanently immobile.")
        return
    try: 
        immobileUnits.remove(unit)
        print(unit, " can now be moved.")
        effect(unit, speedTable, -1)
        effect(unit, gallantryTable, -1)
    except: print(unit, " is not engaged in combat.")

def spy():
    pass

# Army commands

# Naval commands

# Air commands

# Shell functions

# Shell