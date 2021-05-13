# Gamefile for the Battle of the Coral Sea

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

# Unit Types
# Health
health16HP = ["carrier"]
health12HP = ["battleship"]
health10HP = ["crusier"]
health8HP = ["destroyer"]
health4HP = ["corvette", "amphibious"]
health2HP = ["patrol"]
health1HP = ["attack-submarine", "missile-submarine"]
# Movement
movement15cm = ["corvette", "amphibious", "patrol", "attack-submarine", "missile-submarine"]
movement10cm = ["destroyer"]
movement7cm = ["cruiser"]
movement5cm = ["carrier", "battleship"]
headingChange = ["carrier", "destroyer", "battleship", "cruiser", "corvette", "amphibious", "patrol"]
# Depthcharge
depthcharge12 = ["carrier", "battleship"]
depthcharge6 = ["cruiser", "destroyer", "corvette"]
depthchargeable = ["carrier", "battleship", "cruiser", "destroyer", "corvette"]
# Attack
attack4 = ["amphibious", "patrol"]
attack6 = ["corvette"]
attack8 = ["destroyer"]
attack12 = ["carrier"]
attack16 = ["cruiser"]
attack24 = ["battleship"]
attackable = ["amphibious", "patrol", "corvette", "destroyer", "carrier", "cruiser", "battleship"]
# Sortie
sortie8 = ["carrier"]
sortieable = ["carrier"]
# Fire
fire8 = ["battleship"]
fire16 = ["missile-submarine"]
# Search
searchable = ["amphibious", "patrol", "corvette"]
# Torpedo
torpedoable = ["attack-submarine", "missile-submarine"]
# Hide
hideable = ["attack-submarine", "missile-submarine"]
# Move and Fire
moveAndFire = ["carrier", "battleship", "cruiser", "destroyer", "corvette", "amphibious", "patrol"]
# Depthchargable
depthchargeable = ["carrier", "battleship", "cruiser", "destroyer", "corvette"]

def info(unitType):
    if unitType in health1HP:
        print("Health:      1")
    elif unitType in health2HP:
        print("Health:      2")
    elif unitType in health4HP:
        print("Health:      4")
    elif unitType in health8HP:
        print("Health:      8")
    elif unitType in health10HP:
        print("Health:      10")
    elif unitType in health12HP:
        print("Health:      12")
    elif unitType in health16HP:
        print("Health:      16")
    elif unitType in movement5cm:
        print("Movement:    5")
    elif unitType in movement7cm:
        print("Movement:    7")
    elif unitType in movement10cm:
        print("Movement:    10")
    elif unitType in movement15cm:
        print("Movement:    15")
    if unitType in depthcharge6:
        print("Depthcharge: D6")
    elif unitType in depthcharge12:
        print("Depthcharge: D12")
    if unitType in attack4:
        print("Attack:      D4")
    elif unitType in attack6:
        print("Attack:      D6")
    elif unitType in attack8:
        print("Attack:      D8")
    elif unitType in attack12:
        print("Attack:      D12")
    elif unitType in attack16:
        print("Attack:      D16")
    elif unitType in attack24:
        print("Attack:      D24")
    if unitType in sortie8:
        print("Sortie:      D8")
    if unitType in fire8:
        print("Fire:        D8")
    elif unitType in fire16:
        print("Fire:        D16")
    if unitType in searchable:
        print("Can search.")
    if unitType in torpedoable:
        print("Torpedo:     D6")
    if unitType in hideable:
        print("Can hide.")
    if unitType in moveAndFire:
        print("Can move and fire in the same turn.")
    if unitType in headingChange:
        print("Must change heading to alter course.")