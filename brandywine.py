# List units by health points
# HP Chart: infantry, sappers = 4; fusiliers = 6; grenadiers = 8; bombadiers, spyCommand = 10; hussars = 12; dragoons = 16; special forces, highCommand = 20

# French Units
Va1 = Va2 = Va3 = Va5 = Va6 = Va7 = Va9 = Va12 = Pa1 = Pa4 = Pa6 = Pa7 = Pa8 = Nc1 = Md1 = Md2 = Nj2 = Nj4 = 4
Sap1 = Sap2 = 4
Pa1_f = Pa2_f = Pa3_f = Pa4_f = Nj1_f = Nj2_f = Nj3_f = 6
Grn = 8
frenchSpyCommand = 10
Mx1 = Mx2 = 12
Pl = Mc = 16
frenchSpecial1 = frenchSpecial2 = frenchSpecial3 = 20
frenchHighCommand = 20
frenchUnits = [Va1, Va2, Va3, Va5, Va6, Va7, Va9, Va12, Pa1, Pa4, Pa6, Pa7, Pa8, Nc1, Md1, Md2, Nj2, Nj4, Sap1, Sap2, Pa1_f, Pa2_f, Pa3_f, Pa4_f, Nj1_f, Nj2_f, Nj3_f, Grn, frenchSpyCommand, Mx1, Mx2, Pl, Mc, frenchSpecial1, frenchSpecial2, frenchSpecial3, frenchHighCommand]
frenchTotality = 276

# British Units
fourth = fifth = tenth = fifteenth = seventeenth = twentythird = twentyeighth = thirtythird = thirtyeighth = fourtieth = fourtyfourth = sixtyfourth = seventyfirst = seventysecond = seventythird = 4
Gd1 = Gd2 = L_Rg = 4
Eb = Lg = Dp = Wb = Mg = Ls = St = Mb = 6
Grn1 = Grn2 = Grn3 = Grn4 = Grn5 = 8
firstBomb = secondBomb = 10
britishSpyCommand = 10
Lt1 = Lt2 = Lt3 = 12
sixteenthDragoon = seventeenthDragoon = jag = 16
britishSpecial1 = britishSpecial2 = 20
britishHighCommand = 20
britishUnits = [fourth, fifth, tenth, fifteenth, seventeenth, twentythird, twentyeighth, thirtythird, thirtyeighth, fourtieth, fourtyfourth, sixtyfourth, seventyfirst, seventysecond, seventythird, Gd1, Gd2, L_Rg, Eb, Lg, Dp, Wb, Mg, Ls, St, Mb, Grn1, Grn2, Grn3, Grn4, Grn5, firstBomb, secondBomb, britishSpyCommand, Lt1, Lt2, Lt3, britishSpecial1, britishSpecial2, sixteenthDragoon, seventeenthDragoon, jag, britishHighCommand]
britishTotality = 334

# Group units by category
# Type of unit
infantry = [Va1, Va2, Va3, Va5, Va6, Va7, Va9, Va12, Pa1, Pa4, Pa6, Pa7, Pa8, Nc1, Md1, Md2, Nj2, Nj4, fourth, fifth, tenth, fifteenth, seventeenth, twentythird, twentyeighth, thirtythird, thirtyeighth, fourtieth, fourtyfourth, sixtyfourth, seventyfirst, seventysecond, seventythird]
sappers = [Sap1, Sap2, Gd1, Gd2, L_Rg]
fusiliers = [Pa1_f, Pa2_f, Pa3_f, Pa4_f, Nj1_f, Nj2_f, Nj3_f, Eb, Lg, Dp, Wb, Mg, Ls, St, Mb]
grenadiers = [Grn, Grn1, Grn2, Grn3, Grn4, Grn5]
bombadiers = [firstBomb, secondBomb]
hussars = [Mx1, Mx2, Lt1, Lt2, Lt3]
dragoons = [Pl, Mc, sixteenthDragoon, seventeenthDragoon, jag]
special = [frenchSpecial1, frenchSpecial2, frenchSpecial3, britishSpecial1, britishSpecial2]
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

def gameEnd():
    frenchFinal = sum(frenchUnits)
    frenchScore = (frenchFinal / frenchTotality) * 100
    britishFinal = sum(britishUnits)
    britishScore = (britishFinal / britishTotality) * 100
    if frenchScore > britishScore: print("French team wins, with score:", frenchScore, "to", britishScore)
    elif frenchScore < britishScore: print("British team wins, with score:", britishScore, "to", frenchScore)
    else: print("Tie game, with score:", frenchScore, "to", britishScore)