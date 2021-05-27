# At 75 lines of code, the attack(team) function is the longest function in Kriegsspiel. It is a re-write of the previous attack() and defend() functions, which were separate. The separation of offensive and defensive small-arms combat created a negative-damage bug that was not solved until the v2.2 release, with the attack() function.
# This function is callable using the command "attack".

def attack(team): # While the attack command itself takes no arguments, the team whose turn it is is passed to the *function* under the argument "team". Here, "team" is the name of the team (either firstTeam or secondTeam) that is defending.

    # First, the function defines several variables and lists as global. Therefore, the variable firstDamage is understood to be not just defined in this function, but also refers to the global variable by the same name. When the global variables are altered, their values are returned globally when the function ends.
    global immobileUnits # Str list, contains the units that are unable to move in the current turn.
    global usedUnits # Str list, contains the units that have already taken an action in the current turn.
    global deadUnits # Str list, contains the units that are dead.
    global hiddenUnits # Str list, contains the units that are hidden from the battlefield.
    global firstDamage # Int variable, contains the amount of damage the first team has inflicted up to that point in the game.
    global secondDamage # Same as firstDamage, but for the second team.

    # Next, the function defines variables necessary for it to work. These variables are local to the function, and need not be "pushed up" globally when the function ends.
    attackPhase = True # The function consists of two loops. In order for the first loop to be engaged, attackPhase must be set to True.
    defensePhase = False # The second loop executes when defensePhase is set to True. defensePhase does not need to be set as False here; it could be set as True. All that matters is that the variable is defined before the loop.
    totalAttackDamage = 0 # When the attack() function is called, totalAttackDamage is 0 ...
    totalDefenseDamage = 0 # ... as is totalDefenseDamage.
    willQuit = False # In order to enable the user to quit the attack() function if improperly or accidentally called, the function allows for a quit-without-saving subfunction. This is enabled by allowing a "quit" command within the loops. If the user types "quit", this variable is set to True. Here, it is defined as False in order to initialize it.

    # The meat of the function consists of two loops, one for the attack phase and one for the defense phase. Attack phase is first.
    while attackPhase == True: # The loop will end when attackPhase is set to False.
        prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + team + "][attack]% " # The prompt is similar to the one found in the primary game loop, displaying the round number, the command number, and the team that is attacking. At the end, before the %, "[attack]" is added, to ensure that the user understands that this prompt is not the main Kriegsspiel shell, but a subshell.
        attackCommand = input(prompt) # User input is requested using the prompt.
        argsInAttackCommand = attackCommand.split() # argsInAttackComamnd is defined as an integer whose value is the number of words within the user's command.

        # There are two possibilities that are valid: the command could have one word ("help", "quit", "defend") or two words, i.e. the unit and unit type.
        if len(argsInAttackCommand) == 1: # The block of code within this if statement executes if the command is only a single word.
            if attackCommand == "help": # If the user has typed "help", a brief statement about the syntax of the help command is shown.
                print("Syntax: [unit] [unitType]")
                print("'quit' to exit without saving, 'defend' to proceed to defense phase.")
            elif attackCommand == "quit": # If the user has typed "quit" ... 
                attackPhase = False # ... attackPhase is set to False, breaking the current loop as soon as the block of code within this if statement is executed ...
                defensePhase = False # ... defensePhase is set to False, ensuring that the second loop is not executed, and ...
                willQuit = True # ... and willQuit is set to True, so that the quit function is engaged at the end of the function.
            elif attackCommand == "defend": # If the user has typed "defend" ...
                attackPhase = False # ... attackPhase is set to False, breaking the current loop, and ... 
                defensePhase = True # ... defensePhase is set to True, so that the defense loop is engaged.
            else: print("Unknown command.") # If the user has typed anything else, an error is thrown and the loop repeats.
            # After this if statement is gone through, the loop repeats.
    
        elif len(argsInAttackCommand) == 2: # The block of code within this elif statement executies if the command is two words.
            unit, unitType = attackCommand.split() # The user input stored in attackCommand is split into two string variables: unit and unitType, because that is the format required.
            try: # The remainder of this elif block is contained within a try-except statement, since if the user has typed an invalud unitType, Python will throw a valueError and the entire Kriegsspiel program crashes.
                if unit in hiddenUnits: reveal(unit, unitType, team) # If the unit is in the hiddenUnits list, the reveal() function is called.
                maximum = attackTable.get(unitType) + 1 # The maximum value for the attack of this particular unit is calculated by looking up the unitType within the attackTable dictionary provided by the gamefile, which returns the value, and adding one to this value. The increment of 1 is necessary since Python's random.randrange() function uses an exclusive upper bound; e.g. random.randrange(1,6) will never evaluate to 6.
                attackDamage = random.randrange(1, maximum) # The attack damage for that unit is a random value from 1 to the maximum previously defined.
                totalAttackDamage = totalAttackDamage + attackDamage # attackDamage is added to the totalAttackDamage.
                print("Damage dealt:", attackDamage) # The attack damage done by that unit is displayed.
                print("Total damage dealt:", totalAttackDamage) # The total attack damage up to that point is displayed.
                usedUnits.append(unit) # The unit is appended to the list usedUnits, so that it cannot attack again in the current turn.
                immobileUnits.append(unit) # The unit is appended to the list immobileUnits, so that it cannot move later in the current turn.
            except: print("No such unit or unit type.") # Instead of crashing Kriegsspiel, this statement catches the thrown error, displays a simple message, and returns the user to the attack() subshell.

        else: print("Too many arguments.") # If the user inputs more than two words into the attack() subshell, a error is thrown and the user is returned to the subshell.

    # The second loop within the attack() function is mostly the same. Comments will only be added where there is a difference in functionality between the defense phase loop and the attack phase loop
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
            elif defenseCommand == "save": defensePhase = False # The attack() function can only be saved after the defense phase, by typing the function "save". If the user does this, defensePhase is set to False, the loop quits, and the final portion of the function is executed.
            else: print("Unknown command.")
        elif len(argsInDefendCommand) == 2:
            unit, unitType = defenseCommand.split()
            try:
                if unit in hiddenUnits: reveal(unit, unitType, team)
                maximum = attackTable.get(unitType) + 1
                defenseDamage = random.randrange(1, maximum)
                totalDefenseDamage = totalDefenseDamage + defenseDamage
                print("Defense damage dealt: ", defenseDamage)
                print("Total defense damage dealt: ", totalDefenseDamage)
                usedUnits.append(unit)
                immobileUnits.append(unit)
            except: print("No such unit or unit type.")
        else: print("Too many arguments.")

    # The last part of the function is executed after either the quit() or save() commands are executed, breaking out of the loops.
    if willQuit == True: return # If the user at any time typed "quit", willQuit would have been set to True. At this point, if willQuit is true, the function returns a null value and nothing in the gamestate will be altered. Otherwise, the remainder of this block of code will be executed.
    if totalAttackDamage > totalDefenseDamage: damageDealt = totalAttackDamage - totalDefenseDamage # If the total attack damage inflicting during the course of the attack() function being called exceeds the total defense damage, the damage dealt is their difference.
    else: damageDealt = 0 # If the total attack damage is equal to or less than the total defense damage, the damage dealt is 0.
    if team == firstTeam: # If the team passed to the attack() function is the first team as defined in the gamefile ... 
        firstDamage = firstDamage + damageDealt # ... the damage is adjusted accordingly. It should be noted that firstDamage, an integer variable, contains the amount of damage done BY the first team, rather than the amount of damage done TO the first team.
        print(firstTeam, "deal", damageDealt, "damage.") # The team and damage is displayed.
    elif team == secondTeam: # A similar block of code is executed if the team is the second team.
        secondDamage = secondDamage + damageDealt
        print(secondTeam, "deal", damageDealt, "damage.")
    print("If any units were killed in the exchange, call manual(kill).") # Finally, just before the function returns to the main shell, attack() implores the user to enter the command "manual kill" if needed. 