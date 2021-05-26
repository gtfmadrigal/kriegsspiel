def spy(unit, unitType, team):
    global usedUnits
    if not unitType in searchable:
        print("Cannot search.")
        return
    searchEffectiveness = random.randrange(1,7)
    if searchEffectiveness == 6:
        print("Good information.")
        details()
    elif searchEffectiveness == 1:
        print("Bad information.")
        details()
    else: print("No information.")
    usedUnits.append(unit)