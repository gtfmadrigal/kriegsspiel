# score() is a one-word function callable from the shell with the command "score". It is also called by some other functions: details(), fire(), torpedo(), sortie(), depthcharge(), attack() and quitGame().

def score(): # score() is game-wide and takes no functions
    update() # update() is called first, to ensure that the remainder of this function is accurate
    firstPercent = firstHealth / firstHealthTotal * 100 # The percent remaining for each team is equal to the current health, as returned from update(), divided by the totals, multiplied by 100
    secondPercent = secondHealth / secondHealthTotal * 100
    print(firstTeam, "total health:", firstHealth, "or", firstPercent, "%") # health information is displayed
    print(secondTeam, "total health:", secondHealth, "or", secondPercent, "%")