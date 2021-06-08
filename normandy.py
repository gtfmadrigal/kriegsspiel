firstTeam = "Allied"
secondTeam = "Axis"
allUnitTypes = ["infantry", "airborne", "carrier", "battleship", "mechanized", "cavalry"]
airTheater = True
unitTable = {"3rd":"infantry", "51st":"infantry", "50th":"infantry", "47th":"infantry", "1st":"infantry", "29th":"infantry", "4th":"infantry", "7th":"infantry", "6th":"airborne", "101st":"airborne", "82nd":"airborne", "sovereign":"carrier", "lord-of-war":"carrier", "duke-of-cornwall":"battleship", "prince-of-wales":"battleship", "king-george":"battleship", "201st":"infantry", "202nd":"infantry", "203rd":"infantry", "204th":"infantry", "205th":"infantry", "206th":"infantry", "207th":"infantry", "208th":"infantry", "209th":"infantry", "210th":"infantry", "211th":"infantry", "212th":"infantry", "213th":"infantry", "214th":"infantry", "215th":"infantry", "216th":"infantry", "217th":"infantry", "221st":"mechanized", "222nd":"mechanized", "223rd":"mechanized", "224th":"mechanized", "231st":"cavalry", "242th":"cavalry", "261st":"cavalry", "255th":"cavalry"}
firstTeamTable = {"3rd":4, "51st":4, "50th":4, "47th":4, "1st":4, "29th":4, "4th":4, "7th":4, "6th":4, "101st":4, "82nd":4, "sovereign":16, "lord-of-war":16, "duke-of-cornwall":12, "prince-of-wales":12, "king-george":12}
secondTeamTable = {"201st":4, "202nd":4, "203rd":4, "204th":4, "205th":4, "206th":4, "207th":4, "208th":4, "209th":4, "210th":4, "211th":4, "212th":4, "213th":4, "214th":4, "215th":4, "216th":4, "217th":4, "221st":6, "222nd":6, "223rd":6, "224th":6, "231st":16, "242th":16, "261st":16, "255th":16}
firstHealthTotal = 112
secondHealthTotal = 156
firstHealth = sum(firstTeamTable.values())
secondHealth = sum(secondTeamTable.values())
healthTable = {"infantry":4, "airborne":4, "carrier":16, "battleship":12, "mechanized":6, "cavalry":16}
headingTable = {"carrier":1}
moveFireTable = {"infantry":1, "airborne":1, "carrier":1, "battleship":1, "mechanized":1, "cavalry":1}
hideTable = {"infantry":1, "airborne":1}
spyTable = {"infantry":6, "airborne":6, "mechanized":6}
fireTable = {"cavalry":12, "battleship":8}