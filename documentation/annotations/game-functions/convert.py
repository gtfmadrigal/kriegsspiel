# convert() is a game-function callable using the command "convert". It is used to convert a unit from one unitType to another, but it cannot be used to give a unit more power or health.

def convert(unit, unitType, team, targetTeam, targetTeamTable, teamTable): # Ordinary arguments are passed
    global firstTeamTable # The overall unit table and the team tables are made global, since this function alters their values
    global secondTeamTable
    global unitTable
    if unit in firstTeamTable: relevantTable = firstTeamTable # "relevantTable" is mapped to whichever teamTable the unit belongs to.
    elif unit in secondTeamTable: relevantTable = secondTeamTable
    else:
        print(errorMessages.get("team")) # If the unit belongs to no team (which shouldn't happen), an error is thrown and the function returns
        return
    prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + team + "][convert]% " # The prompt includes "[convert]"
    newUnitType = input(prompt) # The function asks for the new unit type.
    if not newUnitType in allUnitTypes: # An error is thrown if the new unit type entered by the user is not valid
        print(errorMessages.get("type"))
        return
    currentHealth = relevantTable.get(unit) # The current health of the unit is retrieved
    maximumHealth = healthTable.get(newUnitType) # The maximum health of the new unit type is retrieved
    if maximumHealth < currentHealth: newHealth = maximumHealth # If the maximum health is less than the current health, the new health is equal to the maximum health
    else: newHealth = currentHealth # Otherwise, the health doesn't change
    relevantTable[unit] = currentHealth # Health is updated
    unitTable[unit] = newUnitType # Unit type is updated
    if unit in hiddenUnits and not newUnitType in hideTable: reveal(unit, unitType, team, targetTeam, targetTeamTable, teamTable) # If the unit is hidden but the new unit type does not allow for hiding, the unit is revealed.