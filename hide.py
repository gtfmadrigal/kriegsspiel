def hide(unit):
    if not globals()[unit] in hide:
        print(unit, "cannot hide.")
        return
    elif globals()[unit] in usedUnits:
        print(unit, "cannot hide.")
        return
    elif globals()[unit] in hiddenUnits:
        print(unit, "is already hidden.")
        return
    secretLocation = input("Location to hide:")
    secrets = secrets + "" + secretLocation
    print(unit, "hidden.")
    hiddenUnits.append(globals()[unit])
    usedUnits.append(globals()[unit])
    immovableUnits.append(globals()[unit])