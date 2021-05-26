def fire(unit, unitType, team):
    global immobileUnits
    global usedUnits
    global deadUnits
    global hiddenUnits
    global firstDamage
    global secondDamage
    if not unitType in fireTable:
        print("Cannot attack.")
        return
    if unit in hiddenUnits:
        print("Unit revealed.")
        reveal(unit, unitType)
    maximum = fireTable.get(unitType) + 1
    damageDealt = random.randrange(1,maximum)
    if team == firstTeam: 
        firstDamage = firstDamage + damageDealt
        print(firstTeam, "deal", damageDealt, "damage.")
    elif team == secondTeam:
        secondDamage = secondDamage + damageDealt
        print(secondTeam, "deal", damageDealt, "damage.")
    print("Manually enter any dead units using the manual(kill) command.")
    usedUnits.append(unit)
    immobileUnits.append(unit)