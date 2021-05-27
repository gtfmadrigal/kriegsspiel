# The depthcharge() function is only used by certain surface ships in naval combat.
# The function is callable from the shell using the command "depthcharge unit unitType."

def depthcharge(unit, unitType, team): # depthcharge() takes three arguments: unit, unitType, and team. Unlike some other commands, the team argument is actually taken, that is, it is actually used in the code, rather than being a mere placeholder.

    # Like many functions, it is divided into three portions: the imports, the checks, and the actual function.
    # The imports pull down various lists and variables from the file itself, allowing the function to affect them globally instead of just locally.
    global immobileUnits # Str list, contains units that have already moved this turn.
    global usedUnits # Str list, contains units that have already taken some combat action this turn.
    global alreadyDropped # Str list, contains units that have already dropped depth charges this turn.
    global firstDamage # Int variable, contains the amount of damage the first team has inflicted up to that point in the game.
    global secondDamage # Same as firstDamage, but for the second team.

    # Checks
    if not unitType in depthchargeable: # If the unit type is not able to drop a depth charge ...
        print("Cannot drop depth charges.") # ... an error message is displayed, and ...
        return # the function returns to the shell without any action being taken.

    if unit in alreadyDropped: # If the unit has already dropped a depth charge this turn ...
        print("Already dropped depth charges.") # ... an error message is displayed, and ...
        return # the function returns to the shell without any action being taken.

    # Actual function
    # Unlike other functions, depthcharge() does not need to look up a maximum in a dictionary, since the maximum is hard-coded at 6
    chargeEffectiveness = random.randrange(1,7) # Note: the maximum for the random.randrange() here is 7, because the Python random.randrange function does not include the upper bound. 7 is never returned.
    if chargeEffectiveness == 6: # Action is only taken if the chargeEffectiveness is 5 or 6. If the chargeEffectiveness is 6 ...
        print("Submarine sunk.") # ... the target submarine is sunk, and a message to that effect displayed to the user ... 
        if team == firstTeam: firstDamage = firstDamage + 1 # ... the damage is added to the first or second team's damage, depending on the team value passed to depthcharge(), the damage only being 1 since that is the HP ascribed to a submarine, and ... 
        elif team == secondTeam: secondDamage = secondDamage + 1
        manual("kill") # ... manual(kill) is called to kill the submarine.

    elif chargeEffectiveness == 5: # If the chargeEffectiveness is 5 ...
        print("Submarine disabled.") # ... the target submarine is disabled, and a message to that effect displayed to the user ...
        disabled = input("Submarine unit disabled: ") # ... the target submarine's name input by the user ...
        immobileUnits.append(disabled) # ... the target submarine is rendered immobile that turn, and ...
        usedUnits.append(disabled) # ... is also considered used for the turn.
    immobileUnits.append(unit) # The ship dropping depth charges is rendered immobile.
    alreadyDropped.append(unit) # The ship dropping depth charges is prevented from dropping another that turn, but not from taking another battle action.