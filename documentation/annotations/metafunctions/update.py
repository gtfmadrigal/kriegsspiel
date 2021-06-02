def update():
    global firstHealth
    global secondHealth
    global firstTeamTable
    global secondTeamTable
    firstHealth = sum(firstTeamTable.values())
    secondHealth = sum(secondTeamTable.values())