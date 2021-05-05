def attack(unit):
    if globals()[unit] in usedUnits:
        print(unit, "cannot attack.")
        return
    elif not globals()[unit] in smallArms:
        print(unit, "cannot attack.")
        return
    multipleUnits = input("Are multiple enemy units being targeted? N/y:")
    if globals()[unit] in d4_smallArms: damage = random.randrange(1,4)
    elif globals()[unit] in d12_smallArms: damage = random.randrange(1,12)
    elif globals()[unit] in d20_smallArms: damage = random.randrange(1,20)
    print(damage, "damage done.")
    if multipleUnits == "y":
        enemyUnit = input("Enemy unit:")
        globals()[enemyUnit] = globals()[enemyUnit] - damage
    else: 
        print("Manually enter damage with the manual command.")