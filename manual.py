def manual(unit):
    print("Manual adjustment commands: newValue, changeList, clearList, exit")
    adjustment = input("Adjustment command: ")
    if adjustment == "newValue":
        newValue = input("New health value: ")
        globals()[unit] = newValue
        if newValue == 0:
            deadUnits.append(globals()[unit])
    elif adjustment == "changeList":
        print("Attribute lists: usedUnits, deadUnits, immovableUnits, hiddenUnits")
        print("Categorical lists: infantry, sappers, fusiliers, grenadiers, bombadiers, hussars, dragoons, special, spy, highCommand")
        newList = input("List to add/remove unit from: ")
        if globals()[unit] in globals()[newList]:
            globals()[newList].remove(globals()[unit])
        else:
            globals()[newList].append(globals()[unit])
    elif adjustment == "clearList":
        print("Attribute lists: usedUnits, deadUnits, immovableUnits, hiddenUnits")
        listToClear = input("List to clear: ")
        globals()[listToClear].clear()
    elif adjustment == "exit":
        return
    else:
        print("Bad command. Try again.")
        return