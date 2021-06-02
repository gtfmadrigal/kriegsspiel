# details() is both an internal meta-function and a callable game function.
# details() is called by spy()
# The command that calls details() from the shell is "details"

def details(): # Details takes no arguments, since it is a game-wide function.
    print("Secrets:")
    print(secrets) # The secrets string is displayed, containing the name and location of every hidden unit
    print("Hidden units:")
    print(*hiddenUnits, sep = ", ") # A simple list of hidden units is shown by displaying the contents of hiddenUnits
    score() # The score() function is called