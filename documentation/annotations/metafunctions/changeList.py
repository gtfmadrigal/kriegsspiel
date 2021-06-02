# changeList function is a meta-function, not callable from the shell
# Since .append, .clear, and .remove already exist, the reason for this function existing is to prevent every function from making every list global. The inclusion of this command in v2.2.35 shortened kriegsspiel.py by 53 lines of code.

def changeList(unit, list, command): # Three arguments are taken, the unit to be appended or removed from the list, the list to be changed, and the command itself, either "append", "clear", or "remove".
    global usedUnits # All lists available in the entire program are made global when this function is called.
    global immobileUnits
    global hiddenUnits
    global alreadyDropped
    global defendingUnits
    global doubleImmobileUnits
    global deadUnits
    if command == "append": list.append(unit) # If the command is "append", the unit is appended to the list.
    elif command == "clear": list.clear() # If the command is "clear", the list is cleared, and the unit argument is irrelevant.
    elif command == "remove": list.remove(unit) # If the command is "remove", the unit is removed from the list.