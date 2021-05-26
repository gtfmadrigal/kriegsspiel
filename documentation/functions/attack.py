
def attack(team):
    global immobileUnits
    global usedUnits
    global deadUnits
    global hiddenUnits
    global firstDamage
    global secondDamage
    attackPhase = True
    defensePhase = False
    totalAttackDamage = 0
    totalDefenseDamage = 0
    willQuit = False
    while attackPhase == True:
        prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + team + "][attack]% "
        attackCommand = input(prompt)
        argsInAttackCommand = attackCommand.split()
        if len(argsInAttackCommand) == 1:
            if attackCommand == "help":
                print("Syntax: [unit] [unitType]")
                print("'quit' to exit without saving, 'defend' to proceed to defense phase.")
            elif attackCommand == "quit": 
                attackPhase = False
                willQuit = True
            elif attackCommand == "defend":
                attackPhase = False
                defensePhase = True
            else: print("Unknown command.")
        elif len(argsInAttackCommand) == 2:
            unit, unitType = attackCommand.split()
            try:
                if unit in hiddenUnits: print("Unit revealed.")
                maximum = attackTable.get(unitType) + 1
                attackDamage = random.randrange(1, maximum)
                totalAttackDamage = totalAttackDamage + attackDamage
                print("Damage dealt:", attackDamage)
                print("Total damage dealt:", totalAttackDamage)
                usedUnits.append(unit)
                immobileUnits.append(unit)
            except: print("No such unit or unit type.")
        else: print("Too many arguments.")
    while defensePhase == True:
        prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + team + "][defense]% "
        defenseCommand = input(prompt)
        argsInDefendCommand = defenseCommand.split()
        if len(argsInDefendCommand) == 1:
            if defenseCommand == "help":
                print("Syntax: [unit] [unitType]")
                print("'quit' to exit without saving, 'save' to save to gamestate.")
            elif defenseCommand == "quit":
                defensePhase = False
                willQuit = True
            elif defenseCommand == "save": defensePhase = False
            else: print("Unknown command.")
        elif len(argsInDefendCommand) == 2:
            unit, unitType = defenseCommand.split()
            try:
                if unit in hiddenUnits: print("Unit revealed.")
                maximum = attackTable.get(unitType) + 1
                defenseDamage = random.randrange(1, maximum)
                totalDefenseDamage = totalDefenseDamage + defenseDamage
                print("Defense damage dealt: ", defenseDamage)
                print("Total defense damage dealt: ", totalDefenseDamage)
                usedUnits.append(unit)
                immobileUnits.append(unit)
            except: print("No such unit or unit type.")
        else: print("Too many arguments.")
    if willQuit == True: return
    if totalAttackDamage > totalDefenseDamage: damageDealt = totalAttackDamage - totalDefenseDamage
    else: damageDealt = 0
    if team == firstTeam:
        firstDamage = firstDamage + damageDealt
        print(firstTeam, "deal", damageDealt, "damage.")
    elif team == secondTeam:
        secondDamage = secondDamage + damageDealt
        print(secondTeam, "deal", damageDealt, "damage.")
    print("If any units were killed in the exchange, call manual(kill).")