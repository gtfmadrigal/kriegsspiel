def reveal(unit, unitType, team):
    global hiddenUnits
    if not unit in hiddenUnits:
        print("Not hidden.")
        return
    hiddenUnits.remove(unit)