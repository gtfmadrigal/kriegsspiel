# This gamefile template is an example, and can be followed along with to create a campaign for your own game.
# First, we need to define some important information about the campaign scenario itself

firstTeam = "" # The team name variables (firstTeam and secondTeam) are strings that are displayed at the shell so that the user knows for which team he is entering commands. These strings should be the capitalized names of the two teams ("Allied" and "Axis", "French" and "British", etc.)
secondTeam = ""
campaign = "" # The campaign variable is a string also displayed at the shell prompt, but for every command in every turn. It can be any length, but should be appropriately capitalized ("Nile", "Brandywine", "Coral Sea", etc.)
airTheater = True # airTheater is a Boolean value that is set to True if there are air units included in the unit table, and False if not
fogOfWar = 1 # fogOfWar is an integer variable. If every command should be interpreted, set it to 1. Otherwise, set fogOfWar to the number of commands for which one should fail, i.e. 4 if 1 in 4 should fail, 10 if 1 in 10 should fail, etc.
warheads = 0 # warheads is the number of nuclear weapons available in a game. Set it to 0 if no "missile-submarine" type units are available, or if you do not want to allow those missile submarines to launch nukes.

# Second, name all of the units

firstTeamTable = {} # List every unit in the first team as string keys, where the values are the integers or floats corresponding to those units' initial health values. They can be the same health value as supplied by the healthTable dictionary in umpire.py, or something else. It's up to you.
secondTeamTable = {}
firstTeamTableOriginal = {} # Simply copy all values from the relevant team table to an original. This is used in some umpire functions to keep track of changes.
secondTeamTableOriginal = {}
locationTable = {} # If desired, list any unit's current location by terrain or structure, but these structures need to be added to the loadGame() function in order to be considered valid by Umpire itself
unitTable = {} # For every unit in firstTeamTable and secondTeamTable, include it here as a string key, where its value is a string corresponding to a given *local* unit type
allUnitTypes = {} # For every local unit type present in unitTable, include it here as a string key, where its value is a string corresponding to a given *universal* unit type, as included in the umpire.py file. If you want to include a new universal unit type in a given campaign, this can be done via the loadGame function (see below)

# Third, calculate the health of the two teams

firstHealthTotal = 0 # The initial health totals must be calculated by using the print() functions below, and must then be added in here manually.
secondHealthTotal = 0
print("First team health total: ", sum(firstTeamTable.values())) # These two print statements will print a summary of every value in the teamTables. They are used to calculate the first and secondHealthTotals. Once done with those tables, simply run this gamefile, take those outputs and put them in the total variables, and then comment out the lines so it is not done every time.
print("Second team health total: ", sum(secondTeamTable.values()))

# Optionally, alter some information about the unit types here:

def loadGame(): # This function is run before the core game loop in umpire.py, then never again
    global movementTable # Set any table you wish to alter to global
    del movementTable["item"] # To delete a unitType from a given table, use this template
    movementTable["item"] = 6 # Use this template to change a unitType's value in a given table
    pass # If you do not wish to alter any of the core functionality of the game, simply include a pass statement and nothing else. The pass statement here is required in order to maintain some code within the function. Note: you cannot simply remove the loadGame() function, as doing so would break the program.