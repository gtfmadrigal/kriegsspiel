
# Air functions
def takeoff(unit, teamFlyingTable):
    if unit in teamFlyingTable:
        print("Already airborne.")
        return
    changeList(unit, teamFlyingTable, "append")

def land(unit, teamFlyingTable):
    changeList(unit, teamFlyingTable, "remove")
    use(unit)

def pulse(unit, unitType, team, targetTeamTable):
    effectiveness = evaluate(unit, unitType, pulseTable)
    if effectiveness == 6:
        print("Pulse effective.")
        pulsePhase = True
        pulsedUnits = []
    elif effectiveness == None: 
        print(errorMessages.get("function"))
        return
    else: 
        print("Pulse ineffective.")
        return
    while pulsePhase == True:
        command = prompt(team, False, "pulse", "player")
        if command in targetTeamTable: pulsedUnits.append(command)
        elif command == "help": print("Enter a unit that has been disabled, 'quit' to exit, or 'save' to exit and save.")
        elif command == "quit": return
        elif command == "save": 
            for x in pulsedUnits: disable(x)
            return
        else: print(errorMessages.get("unit"))
    use(unit)

def airlift(unit, unitType, team, teamTable, teamFlyingTable):
    if not unitType in transportTable:
        print(errorMessages.get("function"))
        return
    liftedUnit = prompt(team, False, "airlift", "player")
    if not liftedUnit in teamTable:
        print(errorMessages.get("team"))
        return
    land(unit, teamFlyingTable)

def kamikaze(unit, unitType, team, teamTable, targetTeamTable):
    global firstTeamTable
    global secondTeamTable
    if not unitType in kamikazeTable:
        print(errorMessages.get("function"))
        return
    target = prompt(team, False, "kamikaze", "player")
    if not target in targetTeamTable:
        print(errorMessages.get("team"))
        return
    effectiveness = evaluate(unit, unitType, kamikazeTable)
    oldHealth = targetTeamTable.get(target)
    if effectiveness == 6 or oldHealth - effectiveness <= 0:
        print(target, "killed.")
        kill(target, targetTeamTable)
    else:
        newHealth = oldHealth - effectiveness
        print(target, "new health:", newHealth)
        targetTeamTable[target] = newHealth
    kill(unit, teamTable)
    score()

# Shell
def info(unit, unitType):
    if not unit in unitTable:
        print(errorMessages.get("team"))
        return
    print("Unit type:", unitTable.get(unit))
    print("Maximum health:", healthTable.get(unitType))
    if unit in firstTeamTable: 
        owner = firstTeam
        print("Current health:", firstTeamTable.get(unit))
        print("Owner:", firstTeam)
    else:
        owner = secondTeam
        print("Current health:", secondTeamTable.get(unit))
        print("Owner:", secondTeam)
    print("Movement:", movementTable.get(unitType))
    print("Attack:", attackTable.get(unitType))
    print("Build:", buildTable.get(unitType))
    print("Sortie:", sortieTable.get(unitType))
    print("Sortie defense:", sortieDefenseTable.get(unitType))
    print("Depth charge:", depthchargeTable.get(unitType))
    if unitType in spyTable: print("Can search.")
    if unitType in hideTable: print("Can hide.")
    if unitType in moveFireTable: print("Can move and fire in the same turn.")
    if unitType in torpedoTable: print("Can fire torpedoes.")
    if unitType in headingTable: print("Heading change required.")
    if unit in immobileUnits: print("Immovable this turn.")
    if unit in usedUnits: print("Unusable this turn.")
    if unit in hiddenUnits: print("Hidden.")

def umpireShell(command, unit):
    if command == "health": health(unit)
    elif command == "kill":
        if unit in firstTeamTable: teamTable = firstTeamTable
        else: teamTable = secondTeamTable
        kill(unit, teamTable)
    elif command == "freeze": freeze(unit)
    elif command == "disable": disable()
    elif command == "merge": merge()
    elif command == "use": use(unit)
    elif command == "split": split()

def airShell(team, targetTeam, teamTable, targetTeamTable, teamFlyingTable, targetTeamFlyingTable):
    global commandNumber
    global airPhase
    rawCommand = prompt(team, True, None, "player")
    if len(rawCommand.split()) == 2:
        command, unit = rawCommand.split()
        localUnitType = unitTable.get(unit)
        unitType = allUnitTypes.get(localUnitType)
        if not unit in unitTable:
            print(errorMessages.get("unit"))
            return
        if unit in deadUnits and not command == "health":
            print(errorMessages.get("dead"))
            return
        if not unitType in flyTable:
            print(errorMessages.get("function"))
            return
        if command in umpireCommands: umpireShell(command, unit)
        elif command in airCommands:
            if not unit in teamTable:
                print(errorMessages.get("team"))
                return
            if unit in deadUnits:
                print(errorMessages.get("dead"))
                return
            if unit in usedUnits:
                print(errorMessages.get("available"))
                return
            if not unit in teamFlyingTable and not command == "takeoff":
                print(errorMessages.get("airborne"))
                return
            if command == "takeoff": takeoff(unit, teamFlyingTable)
            elif command == "land": land(unit, teamFlyingTable)
            elif command == "pulse": pulse(unit, unitType, team, targetTeamTable)
            elif command == "airlift": airlift(unit, unitType, team, teamTable, teamFlyingTable)
            elif command == "survey":spy(unit, unitType)
            elif command == "bomb": fire(unit, unitType, team, targetTeamTable, "bomb", bombTable)
            elif command == "missile": missile(unit, unitType, team, targetTeamTable)
            elif command == "kamikaze": kamikaze(unit, unitType, team, teamTable, targetTeamTable)
            elif command == "split": pass
        else: print(errorMessages.get("bad"))
    elif len(rawCommand.split()) == 1:
        if rawCommand == "dogfight": 
            attack(team, targetTeam, targetTeamFlyingTable, True)
            changeList(True, usedUnits, "clear")
            for x in teamFlyingTable:
                print(x, "crashes.")
                kill(x)
            changeList(True, teamFlyingTable, "clear")
            airPhase = False
        elif rawCommand == "next":
            changeList(True, usedUnits, "clear")
            for x in teamFlyingTable:
                print(x, "crashes.")
                kill(x)
            changeList(True, teamFlyingTable, "clear")
            airPhase = False
        elif rawCommand == "score": score()
        elif rawCommand == "help": helpText()
        elif rawCommand == "details": details()
        elif rawCommand == "quit": quitGame()
        else: 
            print(errorMessages.get("bad"))
            return
    else: 
        print(errorMessages.get("bad"))
        return
    commandNumber = commandNumber + 1
    airShell(team, targetTeam, teamTable, targetTeamTable, teamFlyingTable, targetTeamFlyingTable)

def shell(team, targetTeam, teamTable, targetTeamTable, teamFlyingTable, targetTeamFlyingTable):
    global airPhase
    global commandNumber
    if airPhase == True and airTheater == True: 
        airShell(team, targetTeam, teamTable, targetTeamTable, teamFlyingTable, targetTeamFlyingTable)
        return
    rawCommand = prompt(team, False, None, "player")
    commandFog = fog()
    if commandFog == True:
        print("This command fails.")
        return
    if len(rawCommand.split()) == 2:
        command, unit = rawCommand.split()
        if not unit in unitTable:
            print(errorMessages.get("unit"))
            return
        localUnitType = unitTable.get(unit)
        unitType = allUnitTypes.get(localUnitType)
        if command in umpireCommands: umpireShell(command, unit)
        elif command in navyCommands or command in armyCommands or command in agnosticCommands:
            if not unit in teamTable:
                print(errorMessages.get("team"))
                return
            if unit in deadUnits:
                print(errorMessages.get("dead"))
                return
            if unit in usedUnits:
                print(errorMessages.get("available"))
                return
            if command == "heading": heading(unit, unitType)
            elif command == "torpedo": torpedo(unit, unitType, team, targetTeamTable)
            elif command == "sortie": sortie(unit, unitType, team, targetTeamTable)
            elif command == "depthcharge": depthcharge(unit, unitType, team, targetTeamTable)
            elif command == "build": build(unit, unitType)
            elif command == "missile": missile(unit, unitType, team, targetTeamTable)
            elif command == "move": move(unit, unitType)
            elif command == "hide": hide(unit, unitType, team)
            elif command == "convert": convert(unit, unitType, teamTable)
            elif command == "info": info(unit, unitType)
            elif command == "reveal": reveal(unit, unitType)
            elif command == "spy": spy(unit, unitType)
            elif command == "fire": fire(unit, unitType, team, targetTeamTable, "fire", fireTable)
            elif command == "board": board(unit, unitType, team, teamTable, targetTeamTable)
            else:
                print(errorMessages.get("bad"))
                return
    elif len(rawCommand.split()) == 1:
        if rawCommand == "attack": attack(team, targetTeam, targetTeamTable, False)
        elif rawCommand == "score": score()
        elif rawCommand == "turn": turn()
        elif rawCommand == "quit": quitGame()
        elif rawCommand == "help": helpText()
        elif rawCommand == "merge": merge(team, teamTable)
        elif rawCommand == "details": details()
        else: print(errorMessages.get("bad"))
    else: 
        print(errorMessages.get("bad"))
        return
    commandNumber = commandNumber + 1