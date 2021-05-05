# This is a template for a default gamefile.

# First, give all units a name and assign them a health value
Va1 = 4
# It's a good idea to give units a unique name that is very short, yet as descriptive as possible. Here, the unit called "Virginia First Regiment" becomes Va1. It has four health points.
# Units with the same value can be assigned all at once, as follows:
Va2 = Pa4 = 4
# Create a list that contains all units in the same team, in this case the U.S. Army:
americanUnits = [Va1, Va2, Pa4] # and so on.
# At the end of defining all units for a given team, calculate a totality value, being the sum of the initial health values for a team's entire host
americanTotality = 12

# Do the same for each team.
sovietUnits = []
sovietTotality = 0

# Next, group all units into lists by type. This allows us to create attribute lists later on easier. 
# Suggested lists for modern naval battles: submarines, destroyers, frigates, corvettes, carriers
# Suggested lists for medieval land battles: knights, vagrangian_guard, longbowmen, shortbowmen, peasant_infantry
# Suggested lists for 19th century land battles: infantry, sappers, fusiliers, grenadiers, bombadiers, hussars, dragoons, special. These are the lists used in the default gamefile, brandywine.py
spy = []
highCommand = []
allUnits = [americanUnits, sovietTotality]
# These lists are required.

# Next, create lists by attribute. These lists contain other lists that contain units which have the particular attribute. Various attributes can be given, depending on the game. Some are required:
build = [] # included units can build fortifications. Only needed for land battles
search = [] # included units can search for hidden units. Not needed if there are no hidden units
hide = [] # included units can hide in certain terrain. Not needed if all units are hidden by default, or if units cannot hide
moveAndFire = [] # included units can move and attack (by whatever means) in the same turn. Absolutely required.

# Next, divide units from each attribute list into lists that determine the maximum value when calling the relevant function. For instance, for the build[] list, two lists can be created:
d4_build = [] # these units can create fortifications of strength random.randrange(1,4)
d8_build = [] # these units can create forfications of strength random.randrange(1,8)
# and so on for all attribute lists.

# Finally, a gameEnd function must be created, with that name exactly, that is called when the game is either ended by the umpire or under a scenario otherwise defined.

def gameEnd(): # the gameEnd function takes no arguments
    # First, the function creates the final scores for all teams, where the final score is the ending percent of a team's health points remaining
    americanFinal = sum(americanUnits)
    americanScore = (americanFinal / americanTotality) * 100
    sovietFinal = sum(sovietUnits)
    sovietScore = (sovietFinal / sovietTotality) * 100
    # Second, the function yields different values depending on what team has a higher score
    if americanScore > sovietScore: print("Ameican team wins, with score:", americanScore, "to", sovietScore)
    elif americanScore < sovietScore: print("Soviet team wins, with Score", sovietScore, "to", americanScore)
    else: print("Tie game, both teams have score:", americanScore)
    