# Gamefile fo the Battle of the Brandywine
# Variables
firstTeam = "Rebel"
secondTeam = "British"
validCommands = ["manual", "attack", "fire", "build", "hide", "search", "spy", "info", "manual"]

# Unit types
# Health
health4HP = ["infantry", "sappers"]
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
# Attack
attack4 = ["infantry", "sapper", "fusilier", "grenadier", "bombadier", "spy"]
attack12 = ["hussar"]
attack20 = ["dragoon", "special", "command"]
# Fire
fire8 = ["grenadier"]
fire10 = ["bombadier"]
fire12 = ["hussar"]
fire20 = ["dragoon"]
# Search
searchable = ["infantry", "sapper", "fusilier"]
# Hide
hideable = ["infantry", "sapper", "fusilier", "grenadier", "spy", "special"]
# Move and Fire
moveAndFire = ["infantry", "sapper", "fusilier", "hussar", "dragoon", "special"]

# Prompts
manualHelpPrompt = "Alter Rebel(A) or British health(B) [A/b]: "
ownerPrompt = "Rebel(A) or British(B) unit? [A/b]: "

# info() function
def info(unit):
    # Health
    if unit in health4HP: 
        print("Health:      4")
    elif unit in health6HP: 
        print("Health:      6")
    elif unit in health8HP: 
        print("Health:      8")
    elif unit in health10HP:
        print("Health:      10")
    elif unit in health12HP:
        print("Health:      12")
    elif unit in health16HP:
        print("Health:      16")
    elif unit in health20HP:
        print("Health:      20")
    # Movement
    if unit in movement5cm:
        print("Movement:    5")
    elif unit in movement10cm:
        print("Movement:    10")
    elif unit in movement15cm:
        print("Movement:    15")
    # Attack
    if unit in attack4:
        print("Attack:      D4")
    elif unit in attack12:
        print("Attack:      D12")
    elif unit in attack20:
        print("Attack:      D20")
    # Fire
    if unit in fire8:
        print("Fire:        D8")
    elif unit in fire10:
        print("Fire:        D10")
    elif unit in fire12:
        print("Fire:        D12")
    elif unit in fire20:
        print("Fire:        D20")
    # Search
    if unit in searchable:
        print("Can search.")
    # Hide
    if unit in hideable:
        print("Can hide.")
    # Move and fire
    if unit in moveAndFire:
        print("Can move and fire in the same turn.")


