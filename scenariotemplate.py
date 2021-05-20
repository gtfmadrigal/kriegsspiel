# This is a template file for a gamefile
# When creating a gamefile, give it a unique name.
# Good practice is to list all your gamefiles in your copy of kriegsspiel.py, just under "import random", with the command "from [gamefile] import *" leaving them all commented out. When you want to start a new game, uncomment the line with the gamefile you want. Ordinarily, universal imports are discouraged because of security problems. Since kriegsspiel.py is only importing variables, lists, and a locally defined function, the security issues are nonexistent.

# A gamefile consists of three portions: a section defining the global variables, a section defining the attributes of various unit types, and the info() function. Each will be discussed in turn.

# Global variables defined
firstTeam = "" # Name your first team here in the singular demonymic, e.g. "Rebel", "French", "Soviet", etc.
secondTeam = "" # Name your second team here
validCommands = ["move", "defend", "attack", "info", "manual"] # All valid commands are contained here as strings in a list. move, attack, info, and manual are universal. Others can be added, like "fire", "build", "hide", "search", "spy", "bomb", "torpedo", "launch", and so on, depending on the scenario.
allUnitTypes = [] # All unit types are contained here as strings in a list. This list is never referenced, but it's good practice to keep them here so as not to be confused later. Unit types should be singular.
manualHelpPrompt = ""
ownerPrompt = "" # These prompts are given to the user when calling certain commands. See brandywine.py for more details and an example.
firstDamage = 0 # firstDamage and secondDamage are set to zero initially. These variables store the amount of damage each team has *inflicted* on the other.
secondDamage = 0
firstHealth = 100 # first and secondHealth are standardized values that never change in the course of the game. Their values should be the total health points of each team's units prior to the game.
secondHealth = 100

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
headingChange = [] # This list is required to make the move() function work, but it may be empty. unitTypes included in this list (mostly ships) cannot change heading more than a given amount of degrees in a move() command. If an included unit needs to change heading more than that, the heading() command must be called.
# Attack
attack4 = [] # The example attack damages refer to the *maximum* damage dealt in an attack() command. Again, they can be anything, these are only suggestions.
attack6 = []
attack8 = []
attack10 = []
attack12 = []
attack20 = []
attack24 = [] # all required
attackable = [] # This list contains all types of units contained within the preceding lists. The attack function checks to see if the given unitType is within this list.
# Move and Fire
moveAndFire = [] # This list includes all unit types that can move and fire in the same turn. Not optional.
# Using the above format, you can include various attributes in lists. Just make sure to include them in the info() function. The format should be as follows: "[command][maximum] = []" for all maximum values, followed by "[command]able = []".

# global functions
# info()
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
    if unitType in headingChange:
        print("Must change heading to alter course.")
    if unitType in moveAndFire: # final required attribute, listed at the very end.
        print("Can move and fire in the same turn.")
    
