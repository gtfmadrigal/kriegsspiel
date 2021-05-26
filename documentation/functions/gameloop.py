import random
import os
from manpages import * 
from coralsea import *

round = 1
usedUnits = []
immobileUnits = []
deadUnits = []
commandNumber = 1
secrets = ""
hiddenUnits = []
alreadyDropped = []

while True:
    while (round % 2) != 0:
        prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + firstTeam + "]% "
        rawCommand = input(prompt)
        getCommand(rawCommand, firstTeam)
        commandNumber = commandNumber + 1
    while (round % 2) == 0:
        prompt = "[Rd." + str(round) + "][" + str(commandNumber) + "][" + secondTeam + "]% "
        rawCommand = input(prompt)
        getCommand(rawCommand, secondTeam)
        commandNumber = commandNumber + 1