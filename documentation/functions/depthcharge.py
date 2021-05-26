def depthcharge(unit, unitType, team):
    global immobileUnits
    global usedUnits
    global alreadyDropped
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