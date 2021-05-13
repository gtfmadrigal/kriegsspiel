# Gamefile for the Battle of Agincourt

# Variables
firstTeam = "French"
secondTeam = "British"
validCommands = ["move", "heading", "attack", "fire", "search", "defend", "hide", "reveal", "info", "manual", "build"]
allUnitTypes = ["spearmen", "men-at-arms", "knights", "shortbowmen", "longbowmen", "command", "guard"]
manualHelpPrompt = "Alter French(a) or British health(b)? [a/b: "
ownerPrompt = "French(a) or British (b) unit? [a/b]: "
firstDamage = 0
secondDamage = 0
firstHealth = 215
secondHealth = 180
headingChange = []

# Unit types
# Health
health4HP = ["spearmen", "shortbowmen", "longbowmen"]
health6HP = ["men-at-arms"]
health12HP = ["knights", "command"]
health20HP = ["guard"]
# Movement
movement5cm = ["guard", "command"]
movement10cm = ["spearmen", "shortbowmen", "longbowmen", "men-at-arms"]
movement15cm = ["knights"]
# Attack
attack4 = ["shortbowmen", "longbowmen", "command"]
attack6 = ["spearmen"]
attack8 = ["men-at-arms"]
attack12 = ["guard"]
attack16 = ["knights"]
attackable = ["spearmen", "men-at-arms", "knights", "shortbowmen", "longbowmen", "command", "guard"]
# Fire
fire6 = ["shortbowmen"]
fire12 = ["longbowmen"]
fireable = ["shortbowmen", "longbowmen"]
# Build
build4 = ["spearmen", "men-at-arms"]
buildable = ["spearmen", "men-at-arms"]
# Search
searchable = ["spearmen", "men-at-arms", "knights"]
# Hide
hideable = ["spearmen", "men-at-arms", "shortbowmen", "longbowmen"]
# Move and Fire
moveAndFire = ["spearmen", "men-at-arms", "knights", "guard"]

# info() function
def info(unitType):
    if unitType in health4HP:
        print("Health:      4")
    elif unitType in health6HP:
        print("Health:      6")
    elif unitType in health12HP:
        print("Health:      12")
    elif unitType in health20HP:
        print("Health:      20")
    if unitType in movement5cm:
        print("Movement:    5")
    elif unitType in movement10cm:
        print("Movement:    10")
    elif unitType in movement15cm:
        print("Movement:    15")
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
    if unitType in fire6:
        print("Fire:        D6")
    elif unitType in fire12:
        print("Fire:        D12")
    if unitType in build4:
        print("Build:       D4")
    if unitType in searchable:
        print("Can search.")
    if unitType in hideable:
        print("Can hide.")
    if unitType in moveAndFire:
        print("Can move and fire in the same turn.")