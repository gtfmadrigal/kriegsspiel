# This template can be used to creata a new gamefile.

# Definition of teams
firstTeam = "" # Name of the first team. Should be capitalized.
secondTeam = "" # Name of the second team

# Basic lists
validCommands = ["move", "info", "kill", "man", "health", "freeze", "convert"] # Include all valid commands you want to allow units to call. These seven are mandatory. All valid commands possible are: fire, build, hide, spy, reveal, heading, depthcharge, sortie, and torpedo. Decide which should be included in your game.
allUnitTypes = [] # List all possible unit types here.
airTheater = False

# Universal dictionary
unitTable = {} # Make a massive dictionary here of all units and unit types. The keys should be the names of the units (with each one being unique), and the values should be the unit types. Make sure all keys and values are strings, and that all values here are also included in allUnitTypes.

# Team data
firstTeamTable = {} # This dictionary should include all of the units that belong to the first team as keys, where their values are the health they have at the beginning of the game, stored as integers
secondTeamTable = {} # Same thing for the second team.
firstHealthTotal = 100 # Calculate this manually
secondHealthTotal = 100 # Same here
firstHealth = sum(firstTeamTable.values()) # Current health is developed by summing all of the values in the team tables. As such, health modification is done by changing the value associated with a particular unit in a table.
secondHealth = sum(secondTeamTable.values())

# Command tables and lists
# For each of these dictionaries, the keys should be unit types and the values should be the maximum value for that unit type for that relevant command.
healthTable = {} # Value is the initial health
movementTable = {} # Value is the maximum range (not used in kriegsspiel except for info())
attackTable = {} # Value is the maximum damage dealt per turn in small-arms
sortieTable = {} # Value is the maximum damage a sortie can deal in a turn
sortieDefenseTable = {} # Value is the maximum defense against a sortie
fireTable = {} # Value is the maximum artillery damage
headingTable = {} # Value is always 1 for a given key
spyTable = {} # Value is always 6 for a given key
torpedoTable = {} # Value is always 6 for a given key
hideTable = {} # Value is always 1 for a given key
buildTable = {} # Value is maximum fortification strength
depthchargeTable = {} # Value i always 6 for a given key
moveAndFire = [] # This list contains the unit types which can move and fire in the same turn.