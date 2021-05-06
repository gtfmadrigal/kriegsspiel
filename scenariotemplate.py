# This is a template file for a gamefile
# When creating a gamefile, give it a unique name.
# Good practice is to list all your gamefiles in your copy of kriegsspiel.py, just under "import random", with the command "from [gamefile] import *" leaving them all commented out. When you want to start a new game, uncomment the line with the gamefile you want.

# A gamefile consists of three portions: a section defining the global variables, a section defining the attributes of various unit types, and an info(unitType) function. Each will be discussed in turn.

# Global variables defined
firstTeam = "" # Name your first team here in the singular demonymic, e.g. "Rebel", "French", "Soviet", etc.
secondTeam = "" # Name your second team here
validCommands = ["move", "attack", "info", "manual"] # All valid commands are contained here as strings in a list. move, attack, info, and manual are universal. Others can be added, like "fire", "build", "hide", "search", "spy", "bomb", "torpedo", "launch", and so on, depending on the scenario
allUnitTypes = [] # All unit types are contained here as strings in a list. This list is never referenced, but it's good practice to keep them here so as not to be confused later. Unit types should be singular.
manualHelpPrompt = ""
ownerPrompt = "" # These prompts are given to the user when calling the manual() command. See brandywine.py for more details and an example.

# Attributes of the various units
# Health
health4HP = [] # These lists contain the unit types as strings. The example healths are the various D&D dice, since that is what paper Kriegsspiel is played with, but the values can be anything.
health6HP = []
health8HP = []
health10HP = []
health12HP = []
health20HP = []
# Movement
movement5cm = [] # These lists give the distance different unit types can move in a single turn.
movement10cm = []
movement15cm = []
# Attack
attack4 = [] # The example attack damages refer to the *maximum* damage dealt in an attack() command. Again, they can be anything, these are only suggestions.
attack6 = []
attack8 = []
attack10 = []
attack12 = []
attack20 = []
# Move and Fire
moveAndFire = [] # This list includes all unit types that can move and fire in the same turn. Not optional.
# Using the above format, you can include various attributes in lists. Just make sure to include them in the info() function.

# info() function
def info(unitType): # info() calls only the unitType argument, as the name is irrelevant.
    # Health attribute
    if unitType in health4HP: 
        print("Health:      4")
    # ... continued for each possible health value.
    # Movement attribute
    if unitType in movement5cm:
        print("Movement:    5")
    # ... continued for each possible movement value.
    # Attack attribute
    if unitType in attack4:
        print("Attack:      D4")
    # ... continued for each possible attack value.
    # ... continued for each attribute and attribute value.
    if unitType in moveAndFire: # final required attribute, listed at the very end.
        print("Can move and fire in the same turn.")
