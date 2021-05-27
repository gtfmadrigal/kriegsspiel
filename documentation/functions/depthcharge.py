# The depthcharge() function is only used by certain surface ships in naval combat.
# The function is callable from the shell using the command "depthcharge unit unitType."

def depthcharge(unit, unitType, team): # depthcharge() takes three arguments: unit, unitType, and team. Unlike some other commands, the team argument is actually taken, that is, it is actually used in the code, rather than being a mere placeholder.

    # Like many functions, it is divided into three portions: the imports, the checks, and the actual function.
    # The imports pull down various lists and variables from the file itself, allowing the function to affect them globally instead of just locally.
    global immobileUnits # Str list, contains units that have already moved this turn.
    global usedUnits # Str list, contains units that have already taken some combat action this turn.
    global alreadyDropped # Str list, contains units that have already dropped depth charges this turn.
    
    global firstDamage
    global secondDamage
    if not unitType in depthchargeable:
        print("Cannot drop depth charges.")
        return
    if unit in alreadyDropped:
        print("Already dropped depth charges.")
        return
    chargeEffectiveness = random.randrange(1,7)
    if chargeEffectiveness == 6:
        print("Submarine sunk.")
        if team == firstTeam: firstDamage = firstDamage + 1
        elif team == secondTeam: secondDamage = secondDamage + 1
        manual("kill")
    elif chargeEffectiveness == 5:
        print("Submarine disabled.")
        disabled = input("Submarine unit disabled: ")
        immobileUnits.append(disabled)
        usedUnits.append(disabled)
    immobileUnits.append(unit)
    alreadyDropped.append(unit)