from Poker import *

totalDiff = 0.
totalSDiff = 0.
count = 0

for iteration in range(10):
	game = Game(2, 100, 0)
	print handToGUI(game.board)
	# print handToGUI(game.getPlayerCards(0))
	print handToGUI(game.getPlayerCards(1))
	p = [None, None]
	p[1] = RationalAI(game, 1)
	p[1].refreshStandardProb()
	print "SP: ", p[1].standardProb
	print "SPE: ", p[1].standardProbEst
	totalDiff += abs(p[1].standardProb - p[1].standardProbEst)
	totalSDiff += (p[1].standardProb - p[1].standardProbEst) ** 2
	count += 1
	game.flop()
	p[1].refreshStandardProb()
	print "SP: ", p[1].standardProb
	print "SPE: ", p[1].standardProbEst
	totalDiff += abs(p[1].standardProb - p[1].standardProbEst)
	totalSDiff += (p[1].standardProb - p[1].standardProbEst) ** 2
	count += 1
	game.turn()
	p[1].refreshStandardProb()
	print "SP: ", p[1].standardProb
	print "SPE: ", p[1].standardProbEst
	totalDiff += abs(p[1].standardProb - p[1].standardProbEst)
	totalSDiff += (p[1].standardProb - p[1].standardProbEst) ** 2
	count += 1
	game.river()
	p[1].refreshStandardProb()
	print "SP: ", p[1].standardProb
	print "SPE: ", p[1].standardProbEst
	totalDiff += abs(p[1].standardProb - p[1].standardProbEst)
	totalSDiff += (p[1].standardProb - p[1].standardProbEst) ** 2
	count += 1

print "totalDiff: ", totalDiff, "totalSDiff: ", totalSDiff, "Count: ", count
print "averageDiff: ", totalDiff / count, "RMS Diff: ", (totalSDiff / count) ** .5

