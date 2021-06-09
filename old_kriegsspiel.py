import random
import os
from nile import *

round = 1
usedUnits = []
immobileUnits = []
hiddenUnits = []
alreadyDropped = []
defendingUnits = []
doubleImmobileUnits = []
deadUnits = []
commandNumber = 1
secrets = ""
oneWordCommands = {"score":"score", "turn":"turn", "quit":"quitGame", "help":"helpText", "attack":"attack", "details":"details"}
errorMessages = {"arguments":"Too many arguments for command. Type 'man' [command] for information.", "os":"Unknown operating system.", "bad":"Bad command. Type 'help' for assistance.", "team":"That unit does not belong to you, or it does not exist.", "available":"That unit is currently unavailable.", "function":"That function is unavailable to this unit.", "heading":"Unit cannot exceed its maximum heading change.", "dead":"Unit is dead.", "type":"No such unit type."}

def info(unit, unitType, team, targetTeam, targetTeamTable, teamTable):
    if not unit in unitTable:
        print(errorMessages.get("team"))
        return
    print("Unit type:", unitTable.get(unit))
    print("Maximum health:", healthTable.get(unitType))
    if unit in firstTeamTable: 
        owner = firstTeam
        print("Current health:", firstTeamTable.get(unit))
        print("Owner:", firstTeam)
    else:
        owner = secondTeam
        print("Current health:", secondTeamTable.get(unit))
        print("Owner:", secondTeam)
    print("Movement:", movementTable.get(unitType))
    print("Attack:", attackTable.get(unitType))
    print("Build:", buildTable.get(unitType))
    print("Sortie:", sortieTable.get(unitType))
    print("Sortie defense:", sortieDefenseTable.get(unitType))
    print("Depth charge:", depthchargeTable.get(unitType))
    if unitType in spyTable: print("Can search.")
    if unitType in hideTable: print("Can hide.")
    if unitType in moveAndFire: print("Can move and fire in the same turn.")
    if unitType in torpedoTable: print("Can fire torpedoes.")
    if unitType in headingTable: print("Heading change required.")
    if unit in immobileUnits: print("Immovable this turn.")
    if unit in usedUnits: print("Unusable this turn.")
    if unit in hiddenUnits: print("Hidden.")