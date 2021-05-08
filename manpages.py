manManual = """
manual(argument)
Meta-function

Allows the umpire to directly alter the attributes of units or teams in their entirety. Four arguments are allowed: "help", "health", "kill", and "freeze." Anything else yields an error.

--help: Lists the valid arguments.

--health:
1. Displays the score by calling the score() function.
2. Requests which team's health to alter.
3. Requests the new health value as an integer.
4. Alters the health value.

--kill:
1. Requests the name of the unit to kill.
2. Requests the current health value of the unit.
3. Places the unit in the deadUnits[] list.
4. Requests the unit's parent team.
5. Alters the overall health of the team accordingly.

--freeze:
1. Requests the name of the unit to freeze.
2. Places the unit in the immobileUnits[] list.
"""
manMan = """
man(argument)
Meta-function

Displays the informational page for the command passed to it.
"""
manScore = """
score()
Meta-function

Displays the damage dealt by each team and the percent remaining of their total initial health points.
"""
manTurn = """
turn()
Pseudo-function

Ends the current turn.

1. Clears the usedUnits[] list, making all units available for use again.
2. Clears the immobileUnits[] list, making all units movable again.
3. Increments the round.
"""
manQuit = """
quit()
Pseudo-function

Ends the game.

1. Calls score().
2. Sets warPhase to False, closing the primary game loop and exiting the script.
"""
manHelp = """
help()
Pseudo-function

Displays all valid commands

1. Displays the universal commands.
2. Displays the commands specified as available in the validCommands[] list.
"""
manDetails = """
details()
Meta-function

Displays relevant game information held in the secrets variable.
"""
manMove = """
move(unit, unitType)
Game function

Moves a unit.

1. Checks if unit is in the list immobileUnits[], in which case the function throws an error and quits.
2. Checks if unitType is not in the list moveAndFire[], in which case the unit is added to the list usedUnits[], preventing another command being given to that unit in the current turn.
3. Adds the unit to the immobileUnits[] list, preventing the unit from moving again in the current turn.
"""
manHeading = """
heading(unit, unitType)
Game function

Changes the heading of a unit.

1. Checks if unitType is required to change heading. If not, the function throws an error and quits.
2. Checks if unit is in the list immobileUnits[], in which case the function throws an error and quits.
3. Checks if unitType is not in the list moveAndFire[], in which case the unit is added to the list usedUnits[], preventing another command being given to that unit in the current turn.
4. Adds the unit to the immobileUnits[] list, preventing the unit from moving again in the current turn.
"""
manAttack = """
attack(unit, unitType)
Game function

Primary game function, causes a unit to attack another using its primary weapon, typically small arms.

1. Checks if the unitType has a primary weapon capability. If not, the function throws an error and quits.
2. Checks if the unit is hidden, in which case the reveal(unit, unitType) function is called.
3. Assigns a maximum value for the attack, based on the gamefile.
4. Determines the damage dealt by the attack, by randomly choosing a value from 1 to the maximum.
5. Requests the owner of the unit.
6. Deals the damage to the other team.
7. Adds the unit to the usedUnits[] list.
8. Adds the unit to the immobileUnits[] list.
9. Requests that the user calls the manual function to kill any units that are now dead, and the defend function.
"""
manDefend = """
defend(unit, unitType)
Game function

Reduces damage inflicted by an attack command. Effectively identical to the attack(unit, unitType) function, but inverted.
"""
manFire = """
fire(unit, unitType)
Game function

Inflicts damage based on the secondary weapon of a unit. Functionally similar to attack(unit, unitType). Cannot be defended.
"""
manBuild = """
build(unit, unitType)
Game function

Constructs a fortification.

1. Checks if unitType has building capacity. If not, the function throws an error and quits.
2. Assigns the maximum strength of the fortification based on the capabilities of the unitType.
3. Creates a fortification where the strength is a random number between 1 and the maximum.
4. Adds unit to immobileUnits[].
5. Adds unit to usedUnits[].
"""
manHide = """
hide(unit, unitType)
Game function

Hides unit from the enemy.

1. Checks if unitType has the ability to hide. If not, the function throws an error and quits.
2. Checks if unit is already hidden. If it is, the function throws an error and quits.
3. Adds unit to the hiddenUnits[] list.
4. Requests information about the location of the hidden unit.
5. Adds the information to the secrets variable.
"""
manReveal = """
reveal(unit, unitType)
Game function

Reveals a hidden unit.

1. Checks if unit is not hidden, in which case the function throws an error and quits.
2. Removes the unit from the hiddenUnits[] list.
"""
manSpy = """
spy(unit, unitType)
Game function

Causes a unit to search for hidden units. Information is then passed on to the player at the umpire's discretion.

1. Checks if the unitType has the ability to search. If not, the function throws an error and quits.
2. Randomly determines the search effectiveness between 1 and 6.
3. If the effectiveness is 6: tells the umpire to give good information, and calls details().
4. If the effectiveness is 1: tells the umpire to give wrong information, and calls details().
5. If the effectiveness is 2, 3, 4, or 5: tells the umpire to give no information.
6. Adds the unit to the usedUnits[] list.
"""
manTorpedo = """
torpedo(unit, unitType)
Game function

Causes a unit to fire a torpedo.

1. Checks if the unitType has the ability to fire torpedoes. If not, the function throws an erorr and quits.
2. Generates a torpedo effectiveness number between 1 and 6. If the number is six, manual(kill) is called. If the number is anything else, attack() is called.
3. Adds the unit to the usedUnits[] and immobileUnits[] lists.
"""
manSortie = """
sortie(unit, unitType)
Game function

Causes a unit to launch a sortie.

1. Checks if the unitType has the ability to launch sorties. If not, the function throws an error and quits.
2. Checks if the unit has already been used that turn, in which case the function throws an error and quits.
3. Deals damage equal to a random number between 1 and the maximum dictated by the unitType.
4. Adds the unit to the usedUnits[] and immobileUnits[] lists.
"""
manDepthcharge = """
depthcharge(unit, unitTye)
Game function

Causes a unit to drop a depthcharge in order to sink a submarine.

1. Checks if the unitType has the ability to drop depthcharges. If not, the function throws an error and quits.
2. Checks if the unit has already dropped a depthcharge this turn, in which case the function throws an error and quits.
3. Generates a charge effectiveness between 1 and 6.
4. If the charge effectiveness is 6, the submarine is sunk, damage is altered, and manual(kill) is called.
5. If the charge effectiveness is 5, the submarine is disabled, and added to the immobileUnits[] and usedUnits[] lists.
6. If the charge effectiveness is anything else, nothing happens.
7. The unit dropping the depthcharge is added to immobileUnits[].
"""