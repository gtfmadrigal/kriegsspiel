# Gamefile for the Battle of the Brandywine
import random

# Variables
firstTeam = "Rebel"
secondTeam = "British"
validCommands = ["move", "attack", "fire", "build", "hide", "spy", "info", "manual", "reveal"]
allUnitTypes = ["infantry", "sapper", "fusilier", "grenadier", "bombadier", "hussar", "dragoon", "spy", "special", "command"] # Never used, only kept here for redundancy's sake
manualHelpPrompt = "Alter Rebel(a) or British health(b)? [a/b]: "
ownerPrompt = "Rebel(a) or British(b) unit? [a/b]: "
firstDamage = 0
secondDamage = 0
firstHealth = 276
secondHealth = 334
testVariable = 0

# Unit dictionaries
healthTable = {"infantry":4, "sapper":4, "fusilier":6, "grenadier":8, "bombadier":10, "spy":10, "hussar":12, "dragoon":16, "special":20, "command":20}
movementTable = {"bombadier":5, "dragoon":5, "spy":5, "command":5, "infantry":10, "sapper":10, "grenadier":10, "hussar":10, "special":10, "fusilier":15}
headingChange = []
attackTable = {"infantry":4, "sapper":4, "fusilier":4, "grenadier":4, "bombadier":4, "spy":4, "hussar":12, "dragoon":20, "special":20, "command":20}
fireTable = {"grenadier":8, "bombadier":10, "hussar":12, "dragoon":20}
buildTable = {"infantry":4, "sapper":8}
searchable = ["infantry", "sapper", "fusilier"]
hideable = ["infantry", "sapper", "fusilier", "grenadier", "spy", "special"]
moveAndFire = ["infantry", "sapper", "fusilier", "hussar", "dragoon", "special"]

# info() function
def info(unitType):
    print("Health: ", healthTable.get(unitType))
    print("Movement: ", movementTable.get(unitType))
    print("Attack: ", attackTable.get(unitType))
    print("Build: ", buildTable.get(unitType))
    if unitType in searchable: print("Can search.")
    if unitType in hideable: print("Can hide.")
    if unitType in moveAndFire: print("Can move and fire in the same turn.")