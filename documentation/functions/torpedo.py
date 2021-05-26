def torpedo(unit, unitType, team):
    global usedUnits
    global immobileUnits
    global firstDamage
    global secondDamage
    if team != firstTeam and team != secondTeam:
        print("No such team.")
        return
    if not unitType in torpedoable:
        print("Cannot launch torpedoes.")
        return
    torpedoEffectiveness = random.randrange(1,7)
    if torpedoEffectiveness == 6:
        print("Ship sunk.")
        manual("kill")
    else:
        if team == firstTeam: 
            firstDamage = firstDamage + torpedoEffectiveness
            print(firstTeam, "deal", torpedoEffectiveness, "damage.")
        elif team == secondTeam:
            secondDamage = secondDamage + torpedoEffectiveness
            print(secondTeam, "deal", torpedoEffectiveness, "damage.")
        print("Manually enter any dead units using the manual(kill) command.")
        print("Call defend() function if relevant.")
    usedUnits.append(unit)
    immobileUnits.append(unit)