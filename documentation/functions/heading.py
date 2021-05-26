def heading(unit, unitType, team):
    global immobileUnits
    global usedUnits
    if not unitType in headingChange:
        print("Heading change not required.")
        return
    if unit in immobileUnits:
        print("Immovable.")
        return
    if not unitType in moveAndFire: usedUnits.append(unit)
    immobileUnits.append(unit)