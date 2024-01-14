import random
import sys

# set strings

# import data from gamefile

# create lists
hiddenUnits = []
hideTable = ["lightInfantry", "mediumInfantry", "heavyInfantry", "special", "engineer", "spy", "command", "lightArtillery", "mediumArtillery", "heavyArtillery", "attackSubmarine", "ballisticSubmarine", "stealthBomber", "recon", "transport", "drone"]
hideableTerrain = ["forest", "jungle", "swamp", "mountain"]
secrets = []

# create dictionaries
terrainTable = {}

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

# Meta-functions

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

# Army commands

# Naval commands

# Air commands

# Shell functions

# Shell