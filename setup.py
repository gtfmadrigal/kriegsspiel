# List units by health points
# HP Chart: infantry, sappers = 4; fusiliers = 6; grenadiers = 8; bombadiers, spyCommand = 10; hussars = 12; dragoons = 16; special forces, highCommand = 20

# French Units

frenchUnits = []
# British Units

britishUnits = []
# Group units by category
# Type of unit
infantry = []
sappers = [] # engineers
fusiliers = [] # mechanized infantry
grenadiers = [] # light artillery
bombadiers = [] # heavy artillery
hussars = [] # light cavalry
dragoons = [] # heavy cavalry
special = [] # special forces
spy = [frenchSpyCommand, britishSpyCommand]
highCommand = [frenchHighCommand, britishHighCommand]
allUnits = [infantry, sappers, fusiliers, grenadiers, bombadiers, hussars, dragoons, special, spy, highCommand]
# Small Arms
d4_smallArms = [infantry, sappers, fusiliers, grenadiers, bombadiers]
d12_smallArms = [hussars, highCommand]
d20_smallArms = [dragoons, special]
smallArms = [d4_smallArms, d12_smallArms, d20_smallArms]
# Artillery
d8_artillery = [grenadiers]
d10_artillery = [bombadiers]
d12_artillery = [hussars]
d20_artillery = [dragoons]
artillery = [d8_artillery, d10_artillery, d12_artillery, d20_artillery]
# Build
d4_build = [infantry]
d8_build = [sappers]
build = [d4_build, d8_build]
# Search
search = [infantry, sappers, fusiliers]
# Hide
hide = [infantry, sappers, fusiliers, grenadiers, special, spy]
# Move and Fire
moveAndFire = [infantry, sappers, fusiliers, hussars, dragoons, special]