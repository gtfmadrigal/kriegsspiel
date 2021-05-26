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

# Unit type attributes
# Unit dictionaries. In every dictionary, the key is the unitType ("infantry", "carrier", "longbowmen", etc.), and the value is the relevant attribute it has.
healthTable = {} # values are health points
movementTable = {} # values are range of motion per turn in centimeters
attackTable = {} # values are maximum amount of damage can be dealt per turn
sortieTable = {} # values are maximum sortie damage
fireTable = {} # values are maximum long-range (artillery, archers, etc.) damage

# Unit lists
searchable = [] # unit types in this list are able to execute the search() command
torpedoable = [] # unit types in this list can launch torpedoes (i.e., are submarines)
hideable = [] # unit types in this list can hide
moveAndFire = [] # unit types in this list can move and fire/attack in the same turn
headingChange = [] # unit types in this list cannot move and change heading in the same turn
depthchargeable = [] # unit types in this list can drop depth charges

# info() function
def info(unitType): # info() calls only the unitType argument, as the name is irrelevant.
    print("Health: "), healthTable.get(unitType)
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