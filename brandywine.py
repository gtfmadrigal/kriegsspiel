# Gamefile for the Battle of the Brandywine
import random

# Variables
firstTeam = "Rebel"
secondTeam = "British"
validCommands = ["move", "attack", "fire", "build", "defend", "hide", "spy", "info", "manual", "reveal"]
allUnitTypes = ["infantry", "sapper", "fusilier", "grenadier", "bombadier", "hussar", "dragoon", "spy", "special", "command"] # Never used, only kept here for redundancy's sake
manualHelpPrompt = "Alter Rebel(a) or British health(b)? [a/b]: "
ownerPrompt = "Rebel(a) or British(b) unit? [a/b]: "
firstDamage = 0
secondDamage = 0
firstHealth = 276
secondHealth = 334 

# Unit types
# Health
health4HP = ["infantry", "sapper"]
health6HP = ["fusilier"]
health8HP = ["grenadier"]
health10HP = ["bombadier, spy"]
health12HP = ["hussar"]
health16HP = ["dragoon"]
health20HP = ["special, command"]
# Movement
movement5cm = ["bombadier", "dragoon", "spy", "command"]
movement10cm = ["infantry", "sapper", "grenadier", "hussar", "special"]
movement15cm = ["fusilier"]
headingChange = []
# Attack
attack4 = ["infantry", "sapper", "fusilier", "grenadier", "bombadier", "spy"]
attack12 = ["hussar"]
attack20 = ["dragoon", "special", "command"]
attackable = ["infantry", "sapper", "fusilier", "grenadier", "bombadier", "hussar", "dragoon", "spy", "special", "command"]
# Fire
fire8 = ["grenadier"]
fire10 = ["bombadier"]
fire12 = ["hussar"]
fire20 = ["dragoon"]
fireable = ["grenadier", "bombadier", "hussar", "dragoon"]
# Build
build4 = ["infantry"]
build8 = ["sapper"]
buildable = ["infantry", "sapper"]
# Search
searchable = ["infantry", "sapper", "fusilier"]
# Hide
hideable = ["infantry", "sapper", "fusilier", "grenadier", "spy", "special"]
# Move and Fire
moveAndFire = ["infantry", "sapper", "fusilier", "hussar", "dragoon", "special"]

# info() function
def info(unitType):
    # Health
    if unitType in health4HP: 
        print("Health:      4")
    elif unitType in health6HP: 
        print("Health:      6")
    elif unitType in health8HP: 
        print("Health:      8")
    elif unitType in health10HP:
        print("Health:      10")
    elif unitType in health12HP:
        print("Health:      12")
    elif unitType in health16HP:
        print("Health:      16")
    elif unitType in health20HP:
        print("Health:      20")
    # Movement
    if unitType in movement5cm:
        print("Movement:    5")
    elif unitType in movement10cm:
        print("Movement:    10")
    elif unitType in movement15cm:
        print("Movement:    15")
    # Attack
    if unitType in attack4:
        print("Attack:      D4")
    elif unitType in attack12:
        print("Attack:      D12")
    elif unitType in attack20:
        print("Attack:      D20")
    # Fire
    if unitType in fire8:
        print("Fire:        D8")
    elif unitType in fire10:
        print("Fire:        D10")
    elif unitType in fire12:
        print("Fire:        D12")
    elif unitType in fire20:
        print("Fire:        D20")
    # Build
    if unitType in build4:
        print("Build:       D4")
    elif unitType in build8:
        print("Build:       D8")
    # Search
    if unitType in searchable:
        print("Can search.")
    # Hide
    if unitType in hideable:
        print("Can hide.")
    # Move and fire
    if unitType in moveAndFire:
        print("Can move and fire in the same turn.")