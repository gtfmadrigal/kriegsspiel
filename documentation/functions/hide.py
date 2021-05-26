def hide(unit, unitType, team):
    global hiddenUnits
    global secrets
    if not unitType in hideable:
        print("Cannot hide.")
        return
    if unit in hiddenUnits:
        print("Already hidden.")
        return
    hiddenUnits.append(unit)
    newSecret = input("Describe information about this command: ")
    secrets = secrets + ", " + newSecret