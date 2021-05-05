def spy(unit):
    if not globals()[unit] in spyUnits:
        print(unit, "cannot spy for information.")
        return
    elif globals()[unit] in usedUnits:
        print(unit, "cannot spy for information.")
        return
    spyEfficacy = random.randrange(1,6)
    usedUnits.append(globals()[unit])
    immovableUnits.append(globals()[unit])
    if spyEfficacy == 1:
        print("Give bad information:")
        print(secrets)
    elif spyEfficacy == 6:
        print("Give perfect information:")
        print(secrets)
    else:
        print("Give no information.")