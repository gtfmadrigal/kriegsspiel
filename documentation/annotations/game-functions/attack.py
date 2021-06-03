# attack() is the most important function in the entire game. It is a one-word command callable with "attack".
# For the purposes of documentation, the version of attack() provided here is more verbose than the one actually in kriegsspiel.py, and it will not run.

def attack(team, targetTeam, targetTeamTable, teamTable): # attack() takes most of the standard arguments except for unit and unitType, which go together. This is because attack() uses multiple units on both the attacking and defending sides, so these arguments need not be passed. 
    # For the purposes of documentation, I've separated the function into the general structure (below), the attack phase loop, the defense phase loop, and the save phase loop.
    global firstTeamTable # Makes the team health tables global, since they are altered by the function
    global secondTeamTable
    attackPhase = True # Initially, attackPhase is set to true, defensePhase to false, and willQuit to false.
    defensePhase = False
    willQuit = False
    totalAttackDamage = 0 # The attack and defense damages are created during their respective loops, but they need to first be set to 0.
    totalDefenseDamage = 0
    while attackPhase == True:
        pass # see the section marked "attack phase" below
    while defensePhase == True:
        pass # see the section marked "defense phase" below
    if willQuit == True: return # willQuit will only be set to true if the player has entered the command "quit" instead of "save". If it is true, the function quits and returns to the shell without any alterations being made to the gamestate.
    if totalDefenseDamage >= totalAttackDamage: # Before anything else is done (damage being calculated, the save phase loop, etc.), attack() firsts checks if the defense damage exceeds or equals the attack damage. If this is the case, nothing else needs to be done, and the function returns to the shell.
        print("Attack repelled by", targetTeam)
        return
    netDamage = totalAttackDamage - totalDefenseDamage # Defense damage is subtracted from the attack damage, yielding the total amount of damage that will be inflicted upon the defending team.
    print("Net damage:", netDamage) 
    perUnitDamage = netDamage / len(defendingUnits) # The damage-per-unit is calculated here by using the length of the defendingUnits list.
    print("Damage per unit:", perUnitDamage)
    for x in defendingUnits: # This save-phase loop is performed for every unit in the defendingUnits list, but only if attackPhase exceeds the defense phase
        oldHealth = targetTeamTable.get(x) # The pre-attack() health for each unit is retrieved
        if oldHealth - perUnitDamage < 0: # If the per-unit damage for each unit is 
            newHealth = 0
            print(x, "killed.")
        else: 
            newHealth = oldHealth - perUnitDamage
            print(x, "new health:", newHealth)
        targetTeamTable[x] = newHealth#
    changeList(True, defendingUnits, "clear") # defendingUnits is cleared
    score() # the score is displayed

# Attack phase loop
prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + team + "][attack]% " # This command requires two subshell prompts, one for the attack phase and one for the defense. It is identical to the ordinary shell but with "[attack]" or "[defend]", appended, so that user knows what to do.
command = input(prompt)
if command == "help": print("Enter a named unit to attack, 'defend' to change to the defense phase, or 'quit' to exit without saving.") # If the user enters help, the function does NOT quit, but rather a brief help menu is displayed to the user.
elif command == "quit": # The "quit" command causes the function to end entirely. 
    attackPhase = False # The attack phase exits;
    defensePhase = False # The defense phase exits; 
    willQuit = True # and the function will quit after the loops.
elif command == "defend": # The "defend" command moves the user over to the defense phase loop, see below
    attackPhase = False
    defensePhase = True
elif command in unitTable: # Apart from "help", "quit", and "defend", the user can simply enter the name of a unit that belongs to the attacking team (the primary use case)
    unitType = unitTable.get(command) # The unitType is acquired from the unitTable.
    attackDamage = evaluate(command, unitType, team, targetTeam, targetTeamTable, teamTable, attackTable) # evaluate() is called in order to evaluate that unit's attack damage
    try: # This block of code is contained within a try block, because evaluate() will return a None value if the unit does not belong to the attacking team. This None-value causes a problem for the addition of atttackDamage to totalAttackDamage, so any Python error is caught by the except-statement.
        totalAttackDamage = totalAttackDamage + attackDamage
        changeList(command, usedUnits, "append") # The unit is now "used"
        if not command in moveAndFire: changeList(command, immobileUnits, "append") # If the unit cannot move and fire, it is also appended to immobileUnits.
    except: pass
    print("Damage dealt:", attackDamage) # The damage dealt and total attack damage is displayed to the user.
    print("Total damage dealt:", totalAttackDamage)
else: print(errorMessages.get("bad")) # If the command is anything else, a bad command error message is displayed.

# Defense phase loop
prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + targetTeam + "][defend]% "
command = input(prompt)
if command == "help": print("Enter a named unit to defend, 'save' to save changes to gamestate, or 'quit' to exit without saving.")
elif command == "quit":
    defensePhase = False
    willQuit = True
elif command == "save": defensePhase = False # In the defense loop, the save command is added, which may be called when the user desires to end the defense loop and proceed to saving.
elif command in unitTable:
    unitType = unitTable.get(command)
    defenseDamage = evaluate(command, unitType, targetTeam, targetTeam, targetTeamTable, targetTeamTable, attackTable)
    try: 
        totalDefenseDamage = totalDefenseDamage + defenseDamage
        changeList(command, defendingUnits, "append")
    except: pass
    print("Defense dealt:", defenseDamage)
    print("Total defense dealt:", totalDefenseDamage)
    if totalDefenseDamage >= totalAttackDamage: defensePhase = False # If at any point defense damage exceeds or equals attack damage, the defense loop and the attack() function more generally end, since the attack has been successfully repelled.
else: print(errorMessages.get("bad"))