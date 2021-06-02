# update() is a non-calable one-word metafunction called when the health must be updated.
# Along with changeList(), evaluate(), throwError() and update(), these functions were added in v2.2.35 in order to reduce lines of code by removing common multi-line subfunctions and placing them in separate meta-functions.

def update(): # update() takes no arguments, since it does not need to.
    global firstHealth # Variables and dictionaries relating to the health of the two teams are made global.
    global secondHealth
    global firstTeamTable
    global secondTeamTable
    firstHealth = sum(firstTeamTable.values()) # The health values for the two teams are calculated by summing every value in their team dictionary. These dictionaries contain every unit belonging to a given team and their current health values.
    secondHealth = sum(secondTeamTable.values())