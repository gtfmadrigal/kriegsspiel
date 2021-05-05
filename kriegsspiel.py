# Imports
import random

# Gamefile contents go here
# French Units
Va1 = Va2 = Va3 = Va5 = Va6 = Va7 = Va9 = Va12 = Pa1 = Pa4 = Pa6 = Pa7 = Pa8 = Nc1 = Md1 = Md2 = Nj2 = Nj4 = 4
Sap1 = Sap2 = 4
Pa1_f = Pa2_f = Pa3_f = Pa4_f = Nj1_f = Nj2_f = Nj3_f = 6
Grn = 8
frenchSpyCommand = 10
Mx1 = Mx2 = 12
Pl = Mc = 16
frenchSpecial1 = frenchSpecial2 = frenchSpecial3 = 20
frenchHighCommand = 20
frenchUnits = [Va1, Va2, Va3, Va5, Va6, Va7, Va9, Va12, Pa1, Pa4, Pa6, Pa7, Pa8, Nc1, Md1, Md2, Nj2, Nj4, Sap1, Sap2, Pa1_f, Pa2_f, Pa3_f, Pa4_f, Nj1_f, Nj2_f, Nj3_f, Grn, frenchSpyCommand, Mx1, Mx2, Pl, Mc, frenchSpecial1, frenchSpecial2, frenchSpecial3, frenchHighCommand]
frenchTotality = 276

# British Units
fourth = fifth = tenth = fifteenth = seventeenth = twentythird = twentyeighth = thirtythird = thirtyeighth = fourtieth = fourtyfourth = sixtyfourth = seventyfirst = seventysecond = seventythird = 4
Gd1 = Gd2 = L_Rg = 4
Eb = Lg = Dp = Wb = Mg = Ls = St = Mb = 6
Grn1 = Grn2 = Grn3 = Grn4 = Grn5 = 8
firstBomb = secondBomb = 10
britishSpyCommand = 10
Lt1 = Lt2 = Lt3 = 12
sixteenthDragoon = seventeenthDragoon = jag = 16
britishSpecial1 = britishSpecial2 = 20
britishHighCommand = 20
britishUnits = [fourth, fifth, tenth, fifteenth, seventeenth, twentythird, twentyeighth, thirtythird, thirtyeighth, fourtieth, fourtyfourth, sixtyfourth, seventyfirst, seventysecond, seventythird, Gd1, Gd2, L_Rg, Eb, Lg, Dp, Wb, Mg, Ls, St, Mb, Grn1, Grn2, Grn3, Grn4, Grn5, firstBomb, secondBomb, britishSpyCommand, Lt1, Lt2, Lt3, britishSpecial1, britishSpecial2, sixteenthDragoon, seventeenthDragoon, jag, britishHighCommand]
britishTotality = 334

# Group units by category
# Type of unit
infantry = [Va1, Va2, Va3, Va5, Va6, Va7, Va9, Va12, Pa1, Pa4, Pa6, Pa7, Pa8, Nc1, Md1, Md2, Nj2, Nj4, fourth, fifth, tenth, fifteenth, seventeenth, twentythird, twentyeighth, thirtythird, thirtyeighth, fourtieth, fourtyfourth, sixtyfourth, seventyfirst, seventysecond, seventythird]
sappers = [Sap1, Sap2, Gd1, Gd2, L_Rg]
fusiliers = [Pa1_f, Pa2_f, Pa3_f, Pa4_f, Nj1_f, Nj2_f, Nj3_f, Eb, Lg, Dp, Wb, Mg, Ls, St, Mb]
grenadiers = [Grn, Grn1, Grn2, Grn3, Grn4, Grn5]
bombadiers = [firstBomb, secondBomb]
hussars = [Mx1, Mx2, Lt1, Lt2, Lt3]
dragoons = [Pl, Mc, sixteenthDragoon, seventeenthDragoon, jag]
special = [frenchSpecial1, frenchSpecial2, frenchSpecial3, britishSpecial1, britishSpecial2]
spyUnits = [frenchSpyCommand, britishSpyCommand]
highCommand = [frenchHighCommand, britishHighCommand]
allUnits = [infantry, sappers, fusiliers, grenadiers, bombadiers, hussars, dragoons, special, spyUnits, highCommand]
# Small Arms
d4_smallArms = [infantry, sappers, fusiliers, grenadiers, bombadiers]
d12_smallArms = [hussars, highCommand]
d20_smallArms = [dragoons, special]
smallArms = [d4_smallArms, d12_smallArms, d20_smallArms]
# Artillery
d8_artillery = [grenadiers]
d10_artillery = [bombadiers]
d12_artillery = [hussars]
d20_artillery = [dragoons]
artillery = [d8_artillery, d10_artillery, d12_artillery, d20_artillery]
# Build
d4_build = [infantry]
d8_build = [sappers]
build = [d4_build, d8_build]
# Search
search = [infantry, sappers, fusiliers]
# Hide
hide = [infantry, sappers, fusiliers, grenadiers, special, spyUnits]
# Move and Fire
moveAndFire = [infantry, sappers, fusiliers, hussars, dragoons, special]

# Universal variables
warPhase = True
round = 1
usedUnits = []
deadUnits = []
immovableUnits = [highCommand]
commandNumber = 1
secrets = ""
hiddenUnits = []

# Functions
def getCommand(command, unit): # Primary function
    if globals()[unit] in deadUnits:
        print(unit, "is dead.")
        return
    if command == "move": move(unit)
    elif command == "attack": attack(unit)
    elif command == "fire": fire(unit)
    elif command == "build": build(unit)
    elif command == "hide": hide(unit)
    elif command == "search": search(unit)
    elif command == "spy": spy(unit)
    elif command == "convert": convert(unit)
    elif command == "info": info(unit)
    elif command == "manual": manual(unit)
    else: 
        print("Unknown command.")
        return

def move(unit):
    if globals()[unit] in immovableUnits:
        print(unit,"is immovable.")
        return
    print(unit,"is moved.")
    immovableUnits.append(globals()[unit])
    if not globals()[unit] in moveAndFire:
        usedUnits.append(globals()[unit])

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
        enemyUnit = input("Enemy unit:")
        globals()[enemyUnit] = globals()[enemyUnit] - damage
    else:
        print("Manually enter damage with the manual command.")

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
    
def help():
    print("Informational commands: help, info, endGame, details, manual")
    print("Game commands: move, attack, fire, build, hide, search, convert, spy, endTurn")

def info(unit):
    print("Attributes of unit", unit)
    if globals()[unit] in usedUnits: print("Unusable this turn.")
    if globals()[unit] in deadUnits: print("Dead.")
    if globals()[unit] in immovableUnits: print("Immovable this turn.")
    if globals()[unit] in hiddenUnits: print("Hidden.")
    if globals()[unit] in infantry: print("Infantry: 4HP, 10cm movement, D4 small arms, D4 build, can search, hide, and move and fire.")
    if globals()[unit] in sappers: print("Sapper: 4HP, 10cm movement, D4 small arms, D8 build, can search, hide, and move and fire.")
    if globals()[unit] in fusiliers: print("Fusilier: 6HP, 15cm movement, D4 small arms, can search, hide, and move and fire.")
    if globals()[unit] in grenadiers: print("Grenadier: 8HP, 10cm movement, D4 small arms, D8 artillery, can hide.")
    if globals()[unit] in bombadiers: print("Bombadier: 10HP, 5cm movement, D4 small arms, D10 artillery.")
    if globals()[unit] in hussars: print("Hussar: 12HP, 10cm movement, D12 small arms and artillery, can move and fire.")
    if globals()[unit] in dragoons: print("Dragoon: 16HP, 5cm movement, D20 small arms and artillery, can move and fire.")
    if globals()[unit] in special: print("Special: 20HP, 10cm movement, D20 small arms, can hide, and move and fire.")
    if globals()[unit] in spyUnits: print("Spy: 10HP, 5cm movement, D4 small arms, always hidden, no special abilities.")
    if globals()[unit] in highCommand: print("High command: 20HP, 5cm movement, D20 small arms, immovable.")
    print("Unit value: ", globals()[unit])

def details():
    print(secrets)
    gameEnd()

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

def gameEnd():
    frenchFinal = sum(frenchUnits)
    britishFinal = sum(britishUnits)
    print("French score:", frenchFinal)
    print("British score:", britishFinal)
        
# Game loop
while warPhase == True:
    endGame = False
    turnPortion = 1
    print("Round:", round)
    usedUnits.clear()
    immovableUnits.clear()
    immovableUnits.append(britishHighCommand)
    immovableUnits.append(frenchHighCommand)
    while turnPortion == 1:
        print("Command:", commandNumber)
        command = input("[British]$ ")
        if command == "endTurn": turnPortion = turnPortion + 1
        elif command == "endGame": 
            endGame = True
            break
        elif command == "help": help()
        elif command == "details": details()
        else: 
            unit = input("[unit]$ ")
            getCommand(command, unit)
        commandNumber = commandNumber + 1
    usedUnits.clear()
    immovableUnits.clear()
    immovableUnits.append(highCommand)
    if endGame == True: break
    while turnPortion == 2:
        print("Command:", commandNumber)
        command = input("[French]$ ")
        if command == "endTurn": turnPortion = turnPortion + 1
        elif command == "endGame": 
            endGame = True
            break
        elif command == "help": help()
        elif command == "details": details()
        else: 
            unit = input("[unit]$ ")
            getCommand(command, unit)
        commandNumber = commandNumber + 1
    round = round + 1
    if endGame == True: break

gameEnd()