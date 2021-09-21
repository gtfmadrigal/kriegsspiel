# Definitions
round = 1
commandNumber = 1

# Gamefile
teams = ["amnat", "ruswar", "euromil", "chikor", "indpak", "jewnuc", "islamorg"]
campaign = "WW3"
warheadsTable = {"amnat":100, "ruswar":150, "euromil":100, "chikor":50, "indpak":40, "jewnuc":50, "islamorg":10}
efficiencyTable = {"amnat":0.9, "ruswar":0.75, "euromil":0.65, "chikor":0.7, "indpak":0.6, "jewnuc":0.95, "islamorg":1}
civiliansTable = {"amnat":600000000, "ruswar":350000000, "euromil":100000000, "chikor":180000000, "inpak":200000000, "jewnuc":400000000, "islamorg":10000}
civiliansDead = {"amnat":0, "ruswar":0, "euromil":0, "chikor":0, "indpak":0, "jewnuc":0, "islamorg":0}
civilianEffeciencyTable = {"amnat":0.75, "ruswar":0.75, "euromil":0.7, "chikor":0.8, "indpak":0.55, "jewnuc":0.5, "islamorg":1}
espionageEffeciencyTable = {"amnat":0.75, "ruswar":0.75, "euromil":0.45, "chikor":0.55, "indpak":0.35, "jewnuc":0.95, "islamorg":1}

# Meta functions
def update():
    totalWarheads = sum(warheadsTable.values())

def error():
    pass

def score():
    update()
    print("Warheads")
    for x in warheadsTable:
        print(x, ":", warheadsTable.get(x))
    print("Military efficiency")
    for x in efficiencyTable:
        print(x, ":", efficiencyTable.get(x))
    print("Civilians")
    for x in civiliansTable:
        print(x, ":", civiliansTable.get(x))
    print("Civilian efficiency")
    for x in civilianEffeciencyTable:
        print(x, ":", civilianEffeciencyTable.get(x))
    print("Espionage efficiency")
    for x in espionageEffeciencyTable:
        print(x, ":", espionageEffeciencyTable.get(x))

def dealDamage():
    pass

def save():
    pass

def helpText():
    pass

def quitGame():
    pass

def turn(arguments, team):
    global efficiencyTable
    score()
    if team == "amnat":
        if arguments[1] == "-y":
            if not arguments[2] in teams:
                print("Team does not exist.")
                return
            affectedTeam = arguments[2]
            oldEfficiency = efficiencyTable.get(affectedTeam)
            newEfficiency = oldEfficiency + 0.1
            efficiencyTable[affectedTeam] = newEfficiency
    elif team == "ruswar": pass
    elif team == "euromil": pass
    elif team == "chikor": pass
    elif team == "indpak": pass
    elif team == "jewnuc": pass
    elif team == "islamorg": pass

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

def defend():
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
    elif parsedCommand[0] == "turn": 
        turn(parsedCommand, team)
        return
    elif parsedCommand[0] == "launch": launch()
    elif parsedCommand[0] == "invade": invade()
    elif parsedCommand[0] == "spy": spy()
    elif parsedCommand[0] == "fortify": fortify()
    elif parsedCommand[0] == "draft": draft()
    elif parsedCommand[0] == "defend": defend()
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