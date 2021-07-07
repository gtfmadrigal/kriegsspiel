# Definitions
round = 1
commandNumber = 1
from ww3 import *

# Meta functions
def update():
    pass

def error():
    pass

def score():
    pass

def dealDamage():
    pass

def save():
    pass

def helpText():
    pass

def quitGame():
    pass

# Offensive functions
def launch():
    pass

def invade():
    pass

def spy():
    pass

# Defensive functions
def fortify():
    pass

def block():
    pass

def draft():
    pass

# Special functions
def special():
    pass

# Shell functions
def shell(team):
    global commandNumber
    commandsThisTurn = 0
    validCommand = True
    prompt = str(round) + " ~ " + str(commandNumber) + " " + str(campaign) + "-Air: " + str(team) + " % "
    rawCommand = input(prompt)
    parsedCommand = rawCommand.split()
    if parsedCommand[0] == "score":
        score()
        validCommand = False
        commandNumber = commandNumber + 1
    elif parsedCommand[0] == "help":
        helpText()
        validCommand = False
        commandNumber = commandNumber + 1
    elif parsedCommand[0] == "quit":
        helpText()
        validCommand = False
        commandNumber = commandNumber + 1
    elif parsedCommand[0] == "launch": launch()
    elif parsedCommand[0] == "invade": invade()
    elif parsedCommand[0] == "spy": spy()
    elif parsedCommand[0] == "fortify": fortify()
    elif parsedCommand[0] == "draft": draft()
    elif parsedCommand[0] == "special": 
        special()
        validCommand = False
        commandNumber = commandNumber + 1
    elif parsedCommand[0] == "pass": commandsThisTurn = 2
    else:
        print("No such command.")
        validCommand = False
    if validCommand == True:
        commandNumber = commandNumber + 1
        commandsThisTurn = commandsThisTurn + 1
    score()
    if commandsThisTurn == 2:
        return
    else:
        shell(team)

while True:
    for x in teams:
        shell(x)