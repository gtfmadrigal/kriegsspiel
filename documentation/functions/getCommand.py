def getCommand(rawCommand, team):
    argsInCommand = rawCommand.split()
    if len(argsInCommand) == 4:
        command, unit, unitType = rawCommand.split()
        if command in validCommands:
            if unit in deadUnits:
                print("Dead.")
                return
            elif unit in usedUnits:
                print("Used.")
                return
            if command == "info": 
                info(unitType)
                if unit in deadUnits: print("Dead.")
                if unit in immobileUnits: print("Immovable this turn.")
                if unit in usedUnits: print("Unusable this turn.")
                if unit in hiddenUnits: print("Hidden.")
            else: globals()[command](unit, unitType, team)
        else: print("Unknown command or bad syntax.")
    elif len(argsInCommand) == 2:
        command, argument = rawCommand.split()
        twoWordCommands = ["man", "manual"]
        if command == "manual": manual(argument, team)
        elif command in twoWordCommands: globals()[command](argument)
        else: print("Unknown command or bad syntax.")
    elif len(argsInCommand) == 1:
        oneWordCommands = ["score", "turn", "quit", "help", "attack", "details"]
        if rawCommand in oneWordCommands:
            if rawCommand == "quit": quitGame()
            elif rawCommand == "help": helpText()
            elif rawCommand == "attack": attack(team)
            else: globals()[rawCommand]()
        else: print("Unknown command or bad syntax.")
    else:
        print("A command requires 1 to 3 words.")