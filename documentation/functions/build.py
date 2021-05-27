# The build() function is typically only used by land units, and even then only certain types of land units.
# This function is callable from the shell using the command "build unit unitType."

def build(unit, unitType, team): # The build function takes three arguments: unit, unitType, and team, but the team argument is not used. The team argument is only passed to the build() function by getCommand() in order to unify the process by which functions are called by commands.

    # First, the build() function calls two lists as global, which allows the function to alter these lists globally, rather than just locally.
    global immobileUnits # Str list, contains all units that cannot be moved this turn.
    global usedUnits # Str list, contains all units that cannot have a command passed to them this turn.

    # Since getCommand() checks if the particular unit has already been used in the current turn, all that is necessary for build() to check is if the unitType the unit belongs to is able to build. Ability to build is held in a dictionary called buildTable, where the keys are various unit types as strings, while the values are integers representing the unit type's highest possible built structure strength
    if not unitType in buildTable: # If the unit type is not a key held in the buildTable dictionary ...
        print("Cannot build.") # ... display and error, and ...
        return # ... exit the function without doing anything.
    
    # After the imports and checks, the next part of any function is the actual mathematical function.
    maximum = buildTable.get(unitType) + 1 # The unit type is looked up in the buildTable dictionary, and x.get() returns the value matching the key. The maximum is evaluated by adding 1, to ensure the full functionality of the random.randrange() function.
    fortification = random.randrange(1,maximum) # The built structure, "fortification", has a generated heath value between 1 and the maximum.
    print("Fortification of strength", fortification, "built.") # Information is displayed about the fortification.
    immobileUnits.append(unit) # The unit is immobilized for the remainder of the turn.
    usedUnits.append(unit) # The unit is marked "used" for the remainder of the turn.