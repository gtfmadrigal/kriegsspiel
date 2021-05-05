def fire(unit):
    if globals()[unit] in usedUnits or not globals()[unit] in artillery:
        print(unit, "cannot fire.")
        return
    multipleUnits = input("Are multiple enemy units being targeted? N/y:")
    if globals()[unit] in d8_artillery: damage = random.randrange(1,8)
    elif globals()[unit] in d10_artillery: damage = random.randrange(1,10) 
    elif globals()[unit] in d12_artillery: damage = random.randrange(1,12)
    elif globals()[unit] in d20_artillery: damage = random.randrange(1,20)
    print(damage, "damage done.")
    if multipleUnits == "y":
        enemyUnit = input("[target]% ")
        globals()[enemyUnit] = globals()[enemyUnit] - damage
    else:
        print("Manually enter damage with the manual command.")