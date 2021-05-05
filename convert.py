def convert(unit):
    if not globals()[unit] in artillery:
        print(unit, "cannot be converted or is already infantry.")
        return
    elif globals()[unit] in usedUnits:
        print(unit, "cannot be converted or is already infantry.")
        return
    elif globals()[unit] in grenadiers: grenadiers.remove(globals()[unit])
    elif globals()[unit] in bombadiers: bombadiers.remove(globals()[unit])
    elif globals()[unit] in hussars: hussars.remove(globals()[unit])
    elif globals()[unit] in dragoons: dragoons.remove(globals()[unit])
    infantry.append(globals()[unit])
    usedUnits.append(globals()[unit])
    immovableUnits.append(globals()[unit])