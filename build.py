def build(unit):
    if not globals()[unit] in build:
        print(unit, "cannot build.")
        return
    elif globals()[unit] in usedUnits:
        print(unit, "cannot build.")
        return
    if globals()[unit] in d4_build: fortificationStrength = random.randrange(1,4)
    elif globals()[unit] in d8_build: fortificationStrength = random.randrange(1,8)
    print("Fortification of strength", fortificationStrength, "built.")
    usedUnits.append(globals()[unit])
    immovableUnits.append(globals()[unit])