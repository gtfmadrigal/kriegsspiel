def manual(argument, team):
    global firstDamage
    global secondDamage
    global deadUnits
    global immobileUnits
    if argument == "help": print("Arguments for manual() function: health, kill, freeze.")
    elif argument == "health":
        score()
        teamToChange = input(manualHelpPrompt)
        newValue = int(input("New health value: "))
        if teamToChange == "b": firstDamage = secondHealth - newValue
        else: secondDamage = firstHealth - newValue
    elif argument == "kill":
        namedUnit = input("Name of unit: ")
        currentValue = int(input("Current value of unit: "))
        deadUnits.append(namedUnit)
        if team == secondDamage: firstDamage = firstDamage + currentValue
        elif team == firstDamage: secondDamage = secondDamage + currentValue
    elif argument == "freeze":
        namedUnit = input("Name of unit: ")
        immobileUnits.append(namedUnit)
    else:
        print("Bad argument for manual function.")
        return