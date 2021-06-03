# build() is called from "build", and is used to create fortifications and buildings in the land theater.

def build(unit, unitType, team, targetTeam, targetTeamTable, teamTable): # build() takes the standard arguments
    fortification = evaluate(unit, unitType, team, targetTeam, targetTeamTable, teamTable, buildTable) # The strength of the fortification is calculated using the evaluate() command
    if type(fortification) is int: # If the fortification variable is of integer type (which only happens if the unit is contained within the buildTable dictionary)
        print("Fortification of strength", fortification, "built.")
        changeList(unit, usedUnits, "append")
        changeList(unit, immobileUnits, "append")
    else: 
        print(errorMessages.get("function"))
        return