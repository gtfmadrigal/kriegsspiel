def build(unit, unitType, team):
    global immobileUnits
    global usedUnits
    if not unitType in buildTable:
        print("Cannot build.")
        return
    maximum = buildTable.get(unitType) + 1
    fortification = random.randrange(1,maximum)
    print("Fortification of strength", fortification, "built.")
    immobileUnits.append(unit)
    usedUnits.append(unit)