from Poker import *

totalDiff = [0. for i in range(10)]
totalSDiff = [0. for i in range(10)]
count = 0

for iteration in range(2):
	game = Game(2, 100, 0)
	print handToGUI(game.board)
	# print handToGUI(game.getPlayerCards(0))
	print handToGUI(game.getPlayerCards(1))
	p = [None, None]
	p[1] = RationalAI(game, 1)
	p[1].refreshStandardProb()
	print "SP: ", p[1].standardProb
	# print "SPE: ", p[1].standardProbEst
	for i in range(10):
		p[1].refreshStandardProbEst(float(i + 1) / 10)
		print p[1].standardProbEst
		totalDiff[i] += abs(p[1].standardProb - p[1].standardProbEst)
		totalSDiff[i] += (p[1].standardProb - p[1].standardProbEst) ** 2
	count += 1
	game.flop()
	p[1].refreshStandardProb()
	print "SP: ", p[1].standardProb
	# print "SPE: ", p[1].standardProbEst
	for i in range(10):
		p[1].refreshStandardProbEst(float(i + 1) / 10)
		print p[1].standardProbEst
		totalDiff[i] += abs(p[1].standardProb - p[1].standardProbEst)
		totalSDiff[i] += (p[1].standardProb - p[1].standardProbEst) ** 2
	count += 1
	game.turn()
	p[1].refreshStandardProb()
	print "SP: ", p[1].standardProb
	for i in range(10):
		p[1].refreshStandardProbEst(float(i + 1) / 10)
		print p[1].standardProbEst
		totalDiff[i] += abs(p[1].standardProb - p[1].standardProbEst)
		totalSDiff[i] += (p[1].standardProb - p[1].standardProbEst) ** 2
	count += 1
	game.river()
	p[1].refreshStandardProb()
	print "SP: ", p[1].standardProb
	for i in range(10):
		p[1].refreshStandardProbEst(float(i + 1) / 10)
		print p[1].standardProbEst
		totalDiff[i] += abs(p[1].standardProb - p[1].standardProbEst)
		totalSDiff[i] += (p[1].standardProb - p[1].standardProbEst) ** 2
	count += 1

for i in range(10):
	print float(i + 1) / 10
	print "totalDiff: ", totalDiff[i], "totalSDiff: ", totalSDiff[i], "Count: ", count
	print "averageDiff: ", totalDiff[i] / count, "RMS Diff: ", (totalSDiff[i] / count) ** .5
	print " "

