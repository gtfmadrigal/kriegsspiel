# Gamefile for the Battle of the Coral Sea
import random

# Variables
firstTeam = "French"
secondTeam = "British"
validCommands = ["move", "heading", "depthcharge", "attack", "sortie", "fire", "torpedo", "spy", "defend", "hide", "reveal", "info", "manual"]
allUnitTypes = ["carrier", "battleship", "cruiser", "destroyer", "corvette", "amphibious", "patrol", "attack-submarine", "missile-submarine"]
manualHelpPrompt = "Alter French(a) or British(b) health? [a/b]: "
ownerPrompt = "French(a) or British(b) unit? [a/b]: "
firstDamage = 0
secondDamage = 0
firstHealth = 100
secondHealth = 100

# Unit dictionaries
healthTable = {"attack-submarine":1, "missile-submarine":1, "patrol":2, "corvette":4, "amphibious":4, "destroyer":8, "cruiser":10, "battleship":12, "carrier":16}
movementTable = {"carrier":5, "battleship":5, "cruiser":7, "destroyer":10, "corvette":15, "amphibious":15, "patrol":15, "attack-submarine":15, "missile-submarine":15}
attackTable = {"amphibious":4, "patrol":4, "corvette":6, "destroyer":8, "carrier":12, "cruiser":16, "battleship":24}
sortieTable = {"carrier":8}
fireTable = {"battleship":8, "missile-submarine":16}

# Unit lists
searchable = ["amphibious", "patrol", "corvette"]
torpedoable = ["attack-submarine", "missile-submarine"]
hideable = ["attack-submarine", "missile-submarine"]
moveAndFire = ["carrier", "battleship", "cruiser", "destroyer", "corvette", "amphibious", "patrol"]
headingChange = ["carrier", "destroyer", "battleship", "cruiser", "corvette", "amphibious", "patrol"]
depthchargeable = ["cruiser", "destroyer", "corvette", "carrier", "battleship"]

def info(unitType):
    print("Health: ", healthTable.get(unitType))
    print("Movement: ", movementTable.get(unitType))
    print("Attack: ", attackTable.get(unitType))
    print("Sortie: ", sortieTable.get(unitType))
    print("Fire: ", fireTable.get(unitType))
    if unitType in searchable: print("Can search.")
    if unitType in torpedoable: print("Can fire torpedoes.")
    if unitType in hideable: print("Can hide.")
    if unitType in moveAndFire: print("Can move and fire in the same turn.")
    if unitType in headingChange: print("Must change heading to alter course.")
    if unitType in depthchargeable: print("Can drop depth charges.")