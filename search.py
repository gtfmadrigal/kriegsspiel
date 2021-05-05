def search(unit):
    if not globals()[unit] in search:
        print(unit, "cannot search.")
        return
    elif globals()[unit] in usedUnits:
        print(unit, "cannot search.")
        return
    searchEfficacy = random.randrange(1,6)
    if searchEfficacy == 6:
        print("Perfect information.")
    elif searchEfficacy == 1:
        print("Bad information.")
    else:
        print("No information.")
    usedUnits.append(globals()[unit])
    immovableUnits.append(globals()[unit])