# turn() is a one-word function callable from the shell via "turn". It ends the current turn.

def turn(): # turn() is a gamewide function and takes no arguments
    global round # This is made global since it is altered without the use of changeList()
    changeList(True, usedUnits, "clear") # usedUnits is cleared
    changeList(True, immobileUnits, "clear") # immobileUnits is cleared
    changeList(True, alreadyDropped, "clear") # alreadyDropped is cleared
    for x in doubleImmobileUnits: changeList(x, immobileUnits, "append") # Every item in doubleImmobileUnits is added to the immobileUnits list after the latter has been cleared
    changeList(True, doubleImmobileUnits, "clear") # doubleImmobileUnits is cleared
    round = round + 1 # The round is incremented