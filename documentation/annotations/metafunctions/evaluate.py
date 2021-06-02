# evaluate() is a commonly called meta-function for evaluating functions.
# It is not callable from the shell.

def evaluate(unit, unitType, team, targetTeam, targetTeamTable, teamTable, table): # All arguments provided by the shell are passed to evaluate(), so that it can further pass commands.

    # Definitions
    global firstTeamTable # The unit tables for both teams are made global.
    global secondTeamTable

    # Checks
    if not unit in teamTable: # An error is thrown if the unit does not belong to the relevant team.
        throwError("team")
        return
    if unit in immobileUnits or unit in usedUnits: # An error is thrown if the unit is used or immobile.
        throwError("available")
        return
    if unit in deadUnits: # An error is thrown if the unit is dead.
        throwError("dead")
        return

    # Actual function
    if unit in hiddenUnits: # If the error is hidden, an error is not necessarily thrown, but some other work must be done.
        try: reveal(unit, unitType, team, targetTeam, targetTeamTable, teamTable) # The reveal function is called only if the unit is hidden. If evaluate() has been called by hide() or reveal(), this doesn't matter, because reveal() will do the same thing, and hide() will simply re-add the unit to the hiddenUnits list.
        except: pass # If the reveal() call fails, nothing happens, and the function continues.
    if table.get(unitType) == None: return # If the unitType is not in the table passed to evaluate(), a None value is returned to the calling function. Otherwise, the function continues.
    try: maximum = table.get(unitType) + 1 # The maximum value is set equal to the relevant dictionary's value for the passed key unitType, plus one. The plus one is necessary since random.randrange(x,y) will never return the value y.
    except: # If the try statement fails, this means that the unit does not belong to the team, an error is thrown, and the function returns.
        throwError("team")
        return
    damage = random.randrange(1, maximum) # The value that is returned from the evaluate() function is equal to a random number from 1 to the maximum previously acquired.
    return damage