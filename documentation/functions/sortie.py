def sortie(unit, unitType, team):
    global usedUnits
    global immobileUnits
    global firstDamage
    global secondDamage
    if not unitType in sortieTable:
        print("Cannot launch sorties.")
        return
    if unit in hiddenUnits:
        print("Unit revealed.")
        reveal(unit, unitType)
    maximum = sortieTable.get(unitType) + 1
    damageDealt = random.randrange(1,maximum)
    if team == firstTeam: 
        firstDamage = firstDamage + damageDealt
        print(firstTeam, "deal", damageDealt, "damage.")
    elif team == secondTeam:
        secondDamage = secondDamage + damageDealt
        print(secondTeam, "deal", damageDealt, "damage.")
    print("Manually enter any dead units using the manual(kill) command.")
    print("Sorties can be defended against with the defend() command.")
    usedUnits.append(unit)
    immobileUnits.append(unit)