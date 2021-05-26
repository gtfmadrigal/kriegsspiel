def move(unit, unitType, team):
    global immobileUnits
    global usedUnits
    if unit in immobileUnits:
        print("Immovable.")
        return
    if unitType in headingChange: print("Unit cannot exceed its maximum heading change.")
    if not unitType in moveAndFire: usedUnits.append(unit)
    immobileUnits.append(unit)