import random
import sys

# set strings
roundNumber = 1
commandNumber = 1

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
convertTable = ["lightArtilllery", "mediumArtillery", "heavyArtillery", "lightCavalry", "mediumCavalry", "heavyCavalry"]
reorganizeTable = ["lightInfantry", "mediumInfantry", "heavyInfantry", "lightArtillery", "mediumArtillery", "heavyArtillery", "lightCavalry", "mediumCavalry", "heavyCavalry", "spy", "special", "engineer"]

# create dictionaries
attackTable = {"lightInfantry":4, "mediumInfantry":4, "heavyInfantry":6, "special":12, "engineer":4, "spy":4, "command":12, "lightArtillery":4, "mediumArtillery":4, "heavyArtillery":4, "lightCavalry":6, "mediumCavalry":8, "heavyCavalry":10, "amphibious":4, "patrol":4, "corvette":6, "destroyer":8, "carrier":12, "battleship":12, "cruiser":12, "heavyFighter":6, "attackSubmarine":0, "missileSubmarine":0, "lightFighter":4, "bomber":4, "stealthBomber":4, "transport":4, "recon":4, "drone":4}
movementTable = {"foot":1.5, "horse":12, "motor":25, "tank":15, "oar":2, "sail":3, "steam":10, "nuclear":20}
terrainSpeedTable = {"unpaved":1, "paved":2, "forest":-1, "hills":-1, "creek":-2, "denseForest":-2, "steepHills":-2, "swamp":-3, "jungle":-3, "mountains":-3, "plains":0}
spyTable = {"engineers":6, "lightInfantry":8, "mediumInfantry":8, "heavyInfantry":8, "special":10, "spy":10}
fireTable = {"lightArtillery":8, "mediumArtillery":10, "heavyArtillery":12, "lightCavalry":8, "mediumCavalry":10, "heavyCavalry":12, "corvette":6, "cruiser":20, "destroyer":10, "battleship":12}

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

# strength, speed, precision, haste, industry, regeneration, resistance, nobility, vision, silence, wisdom, gallantry

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
firstHealth = sum(firstTeamTable.values())
secondHealth = sum(secondTeamTable.values())
loadGame()

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
    unit = arguments[1]
    if unit in firstTeamTable: firstTeamTable.remove(unit)
    if unit in secondTeamTable: secondTeamTable.remove(unit)
    deadUnits.append(unit)
    strengthTable.remove(unit)
    speedTable.remove(unit)
    precisionTable.remove(unit)
    hasteTable.remove(unit)
    industryTable.remove(unit)
    regenerationTable.remove(unit)
    resistanceTable.remove(unit)
    nobilityTable.remove(unit)
    visionTable.remove(unit)
    silenceTable.remove(unit)
    wisdomTable.remove(unit)
    gallantryTable.remove(unit)

def structureDamage(damage, location, haste):
    global structureStrengthTable
    global terrainTable
    global hiddenUnits
    oldStructureHealth = structureStrengthTable(location)
    if (oldStructureHealth - damage - haste) >= oldStructureHealth: 
        newStructureHealth = oldStructureHealth
    else: newStructureHealth = oldStructureHealth - damage - haste
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

def damage(unit, damage, teamTable, haste):
    global firstTeamTable
    global secondTeamTable
    oldHealth = teamTable.get(unit)
    location = terrainTable.get(unit)
    if location in structureStrengthTable: newDamage = structureDamage(damage, location, haste)
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

def fog():
    if fogOfWar == 1:
        return False
    export = random.randrange(1, (fogOfWar + 1))
    if export == 1: return True
    else: return False

def log():
    originalOutput = sys.stdout
    with open("log.txt", "w") as f:
        sys.stdout = f
        print("Round: ", roundNumber)
        print(firstTeam)
        for x in firstTeamTable:
            strength = "strength: " + str(strengthTable.get(x)) + ", "
            speed = "speed: " + str(speedTable.get(x)) + ", "
            precision = "precision: " + str(precisionTable.get(x)) + ", "
            haste = "haste: " + str(hasteTable.get(x)) + ", "
            industry = "industry: " + str(industryTable.get(x)) + ", "
            regeneration = "regeneration: " + str(regenerationTable.get(x)) + ", "
            nobility = "nobility: " + str(nobilityTable.get(x)) + ", "
            vision = "vision: " + str(visionTable.get(x)) + ", "
            silence = "silence: " + str(silenceTable.get(x)) + ", "
            wisdom = "wisdom: " + str(wisdomTable.get(x)) + ", "
            gallantry = "gallantry: " + str(gallantryTable.get(x)) + ", "
            health = "health: " + str(firstTeamTable.get(x)) + ", "
            try: location = str(terrainTable.get(x)) + ", "
            except: location = "plains, "
            if x in hiddenUnits: hidden = "hidden, "
            else: hidden = "visible, "
            if x in immobileUnits: immobile = "immobile, "
            else: immobile = "mobile"
            if x in usedUnits: used = "used, "
            else: used = "unused, "
            line = str(x) + ": " + str(location) + str(hidden) + str(immobile) + str(used) + str(strength) + str(speed) + str(precision) + str(haste) + str(industry) + str(regeneration) + str(nobility) + str(vision) + str(silence) + str(wisdom) + str(gallantry) + str(health)
            print(line)
        for x in secondTeamTable:
            strength = "strength: " + str(strengthTable.get(x)) + ", "
            speed = "speed: " + str(speedTable.get(x)) + ", "
            precision = "precision: " + str(precisionTable.get(x)) + ", "
            haste = "haste: " + str(hasteTable.get(x)) + ", "
            industry = "industry: " + str(industryTable.get(x)) + ", "
            regeneration = "regeneration: " + str(regenerationTable.get(x)) + ", "
            nobility = "nobility: " + str(nobilityTable.get(x)) + ", "
            vision = "vision: " + str(visionTable.get(x)) + ", "
            silence = "silence: " + str(silenceTable.get(x)) + ", "
            wisdom = "wisdom: " + str(wisdomTable.get(x)) + ", "
            gallantry = "gallantry: " + str(gallantryTable.get(x)) + ", "
            health = "health: " + str(secondTeamTable.get(x)) + ", "
            try: location = str(terrainTable.get(x)) + ", "
            except: location = "plains, "
            if x in hiddenUnits: hidden = "hidden, "
            else: hidden = "visible, "
            if x in immobileUnits: immobile = "immobile, "
            else: immobile = "mobile"
            if x in usedUnits: used = "used, "
            else: used = "unused, "
            line = str(x) + ": " + str(location) + str(hidden) + str(immobile) + str(used) + str(strength) + str(speed) + str(precision) + str(haste) + str(industry) + str(regeneration) + str(nobility) + str(vision) + str(silence) + str(wisdom) + str(gallantry) + str(health)
            print(line)
        print(secrets)
        score()  
    sys.stdout = originalOutput

def score():
    update()
    firstPercent = firstHealth / firstHealthTotal * 100
    secondPercent = secondHealth / secondHealthTotal * 100
    print(firstTeam, "total health:", firstHealth, "or", firstPercent, "%")
    print(secondTeam, "total health:", secondHealth, "or", secondPercent, "%")

def update():
    global firstHealth
    global secondHealth
    global firstTeamTable
    global secondTeamTable
    firstHealth = sum(firstTeamTable.values())
    secondHealth = sum(secondTeamTable.values())

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
    haste = 0
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
        unitType = unitTable.get(x)
        max = attackTable.get(unitType)
        strength = strengthTable.get(x)
        base = random.randrange(1, max)
        total = base + strength
        if total >= max: attackCritical = attackCritical + 1
        totalAttack = totalAttack + total
        if unitTable[x] == "lightInfantry": effect(x, silenceTable, -1)
        if unitTable[x] == "special": effect(x, silenceTable, -1)
        else: effect(x, silenceTable, -2)
        hasteModifier = hasteTable.get(x)
        haste = haste + hasteModifier
        reveal(x)
        immobileUnits.append(x)
        usedUnits.append(x)
    for x in defendingUnits:
        unitType = unitTable.get(x)
        max = attackTable.get(unitType)
        resistance = resistanceTable.get(x)
        base = random.randrange(1, max)
        total = base + resistance
        if total <= 1: 
            total = 1
            defenseCritical = defenseCritical + 1
        totalDefense = totalDefense + total
        if unitTable[x] == "lightInfantry": effect(x, silenceTable, -1)
        if unitTable[x] == "special": effect(x, silenceTable, -1)
        else: effect(x, silenceTable, -2)
        reveal(x)
        immobileUnits.append(x)
        usedUnits.append(x)
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
    for x in defendingUnits: damage(x, perUnitDamage, targetTeamTable, haste)

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
    unit = arguments[1]
    if unit in permanentlyImmobileUnits:
        print(unit, " is permanently immobile.")
        return
    try: 
        immobileUnits.remove(unit)
        print(unit, " can now be moved.")
        effect(unit, speedTable, -1)
        effect(unit, gallantryTable, -1)
    except: print(unit, " is not engaged in combat.")

def spy(arguments):
    global usedUnits
    try: unit = arguments[1]
    except:
        print("Parse error.")
        return
    if unit in usedUnits:
        print(unit, " cannot spy.")
        return
    unitType = unitTable.get(unit)
    if not unitType in spyTable:
        print(unit, " cannot spy.")
        return
    spyMax = spyTable.get(unitType)
    vision = visionTable.get(unit)
    baseQuality = random.randrange(0, spyMax)
    adjQuality = baseQuality + vision
    if adjQuality >= 6: 
        print("Give good intelligence: ")
        print(secrets)
    elif adjQuality <= 2:
        print("Give bad intelligence:")
        print(secrets)
    else: print("Give no information.")
    usedUnits.append(unit)   

def fire(arguments, teamTable, targetTeamTable):
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
    haste = 0
    del arguments[0]
    for x in arguments:
        if x == ">": pass
        elif x in usedUnits: pass
        elif x in teamTable:
            unitType = unitTable.get(x)
            if not unitType in fireTable:
                print("Units of type: ", unitType, " cannot fire.")
                pass
            attackingUnits.append(x)
            if x in hiddenUnits: reveal(x)
        elif x in targetTeamTable: defendingUnits.append(x)
        else: print(x, " does not exist.")
    for x in attackingUnits:
        unitType = unitTable.get(x)
        max = fireTable.get(unitType)
        precision = precisionTable.get(x)
        base = random.randrange(1, max)
        total = base + precision
        totalAttack = totalAttack + total
        if unitTable[x] == "lightInfantry": effect(x, silenceTable, -1)
        if unitTable[x] == "special": effect(x, silenceTable, -1)
        else: effect(x, silenceTable, -2)
        hasteModifier = hasteTable.get(x)
        haste = haste + hasteModifier
        reveal(x)
        if unitType == "lightArtillery": immobileUnits.append(x)
        elif unitType == "mediumArtillery": immobileUnits.append(x)
        elif unitType == "heavyArtillery": immobileUnits.append(x)
        usedUnits.append(x)
    for x in defendingUnits:
        unitType = unitTable.get(x)
        max = attackTable.get[unitType]
        resistance = resistanceTable.get(x)
        base = random.randrange(1, max)
        total = base + resistance
        totalDefense = totalDefense + total
        if unitTable[x] == "lightInfantry": effect(x, silenceTable, -1)
        if unitTable[x] == "special": effect(x, silenceTable, -1)
        else: effect(x, silenceTable, -2)
        reveal(x)
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
    for x in defendingUnits: damage(x, perUnitDamage, targetTeamTable, haste)

# Army commands

def convert(arguments, teamTable):
    global firstTeamTable
    global secondTeamTable
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
    try: 
        unit = arguments[1]
        if arguments[2] == ">": newUnit = arguments[3]
        else: newUnit = arguments[2]
    except:
        print("Invalid number of arguments.")
        return
    unitType = unitTable.get(unit)
    if not unitType in convertTable:
        print("Units of type: ", unitType, " cannot be converted.")
        return
    if not unit in teamTable:
        print(unit, " does not belong to that player.")
        return
    strength = strengthTable.get(unit)
    speed = speedTable.get(unit)
    haste = hasteTable.get(unit)
    industry = industryTable.get(unit)
    regeneration = regenerationTable.get(unit)
    resistance = resistanceTable.get(unit)
    nobility = nobilityTable.get(unit)
    vision = visionTable.get(unit)
    silence = silenceTable.get(unit)
    wisdom = wisdomTable.get(unit)
    gallantry = gallantryTable.get(unit)
    currentHealth = teamTable.get(unit)
    if currentHealth > 4: newHealth = 4
    else: newHealth = currentHealth
    teamTable[newUnit] = newHealth
    unitTable[newUnit] = "lightInfantry"
    strengthTable[newUnit] = strength
    speedTable[newUnit] = speed
    precisionTable[newUnit] = 0
    hasteTable[newUnit] = haste
    industryTable[newUnit] = industry
    regenerationTable[newUnit] = regeneration
    resistanceTable[newUnit] = resistance
    nobilityTable[newUnit] = nobility
    visionTable[newUnit] = vision
    silenceTable[newUnit] = silence
    wisdomTable[newUnit] = wisdom
    gallantryTable[newUnit] = gallantry
    kill(unit)
    update()

def reorganize(arguments, teamTable):
    global firstTeamTable
    global secondTeamTable
    global unitTable
    reorganizedUnits = []
    reorganizedUnitTypeCheck = []
    killedUnits = []
    savedUnits = []
    totalHealth = 0
    for x in arguments:
        if not x in unitTable: pass
        if not x in teamTable: pass
        unitType = teamTable.get(x)
        reorganizedUnits.append(x)
        reorganizedUnitTypeCheck.append(x)
    newUnitType = reorganizedUnitTypeCheck[0]
    try: len(set(reorganizedUnitTypeCheck)) == 1
    except:
        print("Units are not all of the same type.")
        return
    if unitType == "lightInfantry": newHealth = 4
    elif unitType == "engineer": newHealth = 4
    elif unitType == "mediumInfantry": newHealth = 6
    elif unitType == "heavyInfantry": newHealth = 6
    elif unitType == "special": newHealth = 20
    elif unitType == "lightArtillery": newHealth = 6
    elif unitType == "mediumArtillery": newHealth = 7
    elif unitType == "heavyArtillery": newHealth = 8
    elif unitType == "lightCavalry": newHealth = 8
    elif unitType == "mediumCavalry": newHealth = 10
    elif unitType == "heavyCavalry": newHealth = 12
    else:
        print("Units of type ", unitType, " cannot be reorganized.")
        return
    for x in reorganizedUnits:
        health = teamTable.get(x)
        totalHealth = totalHealth + health
    for x in reorganizedUnits:
        health = teamTable.get(x)
        healthDifference = newHealth - health
        totalHealth = totalHealth - healthDifference
        if totalHealth < 0: killedUnits.append(x)
        else:
            teamTable[x] = newHealth
            savedUnits.append(x)
    for x in killedUnits: kill(x)
    for x in savedUnits:
        effect(x, strengthTable, -1)
        effect(x, speedTable, -1)
        effect(x, hasteTable, -1)
    update()

# Naval commands

# Air commands

# Shell functions
def shell(team, teamTable, targetTeamTable):
    global commandNumber
    prompt = str(roundNumber) + " ~ " + str(commandNumber) + " " + str(campaign) + ": " + str(team) + " % "
    rawCommand = input(prompt)
    parsedCommand = rawCommand.parse()
    if fog() == True:
        print("This command fails.")
        commandNumber = commandNumber + 1
        return
    if not parsedCommand:
        print("This command does not exist.")
        commandNumber = commandNumber + 1
        return
    elif parsedCommand[0] == "kill": kill(parsedCommand)
    elif parsedCommand[0] == "effect":
        amount = parsedCommand[3]
        try: fakeAmount = amount + 1
        except: 
            print("Not an integer amount.")
            return
        unit = parsedCommand[1]
        if parsedCommand[2] == "strength": effect(unit, strengthTable, amount)
        elif parsedCommand[2] == "speed": effect(unit, speedTable, amount)
        elif parsedCommand[2] == "precision": effect(unit, precisionTable, amount)
        elif parsedCommand[2] == "haste": effect(unit, hasteTable, amount)
        elif parsedCommand[2] == "industry": effect(unit, industryTable, amount)
        elif parsedCommand[2] == "regeneration": effect(unit, regenerationTable, amount)
        elif parsedCommand[2] == "resistance": effect(unit, resistanceTable, amount)
        elif parsedCommand[2] == "nobility": effect(unit, nobilityTable, amount)
        elif parsedCommand[2] == "vision": effect(unit, visionTable, amount)
        elif parsedCommand[2] == "silence": effect(unit, silenceTable, amount)
        elif parsedCommand[2] == "wisdom": effect(unit, wisdomTable, amount)
        elif parsedCommand[2] == "gallantry": effect(unit, gallantryTable, amount)
        else: 
            "No such effect."
            return
    elif parsedCommand[0] == "hide": hide(parsedCommand)
    elif parsedCommand[0] == "reveal": reveal(parsedCommand)
    elif parsedCommand[0] == "attack": attack(parsedCommand, teamTable, targetTeamTable)
    elif parsedCommand[0] == "move": move(parsedCommand, teamTable)
    elif parsedCommand[0] == "disengage": disengage(parsedCommand)
    elif parsedCommand[0] == "spy": spy(parsedCommand)
    elif parsedCommand[0] == "log": log()
    elif parsedCommand[0] == "score": score()
    elif parsedCommand[0] == "update": update()
    elif parsedCommand[0] == "fire": fire(parsedCommand, teamTable, targetTeamTable)
    elif parsedCommand[0] == "convert": convert(parsedCommand, teamTable)
    elif parsedCommand[0] == "reorganize": reorganize(parsedCommand, teamTable)
    else: print("No such command.")
    log()

# Shell
while True: 
    while (round % 2) != 0: shell(firstTeam, firstTeamTable, secondTeamTable)
    while (round % 2) == 0: shell(secondTeam, secondTeamTable, firstTeamTable)