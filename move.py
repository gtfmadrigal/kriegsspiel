def move(unit):
    if globals()[unit] in immovableUnits:
        print(unit,"is immovable.")
        return
    print(unit,"is moved.")
    immovableUnits.append(globals()[unit])
    if not globals()[unit] in moveAndFire:
        usedUnits.append(globals()[unit])