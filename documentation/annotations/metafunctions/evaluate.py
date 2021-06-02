# evaluate() is a commonly called meta-function for evaluating functions.
# It is not callable from the shell.

def evaluate(unit, unitType, team, targetTeam, targetTeamTable, teamTable, table): # All arguments provided by the shell are passed to evaluate(), so that it can further pass commands.
    global firstTeamTable
    global secondTeamTable
    if not unit in teamTable:
        throwError("team")
        return
    if unit in immobileUnits or unit in usedUnits:
        throwError("available")
        return
    if unit in deadUnits:
        throwError("dead")
        return
    if unit in hiddenUnits:
        if table == hideTable: pass
        else:
            try: reveal(unit, unitType, team, targetTeam, targetTeamTable, teamTable)
            except: pass
    if table.get(unitType) == None: return
    try: maximum = table.get(unitType) + 1
    except:
        throwError("team")
        return
    damage = random.randrange(1, maximum)
    return damage