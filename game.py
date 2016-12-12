from Poker import *
import sys

if len(sys.argv) < 2:
	print "Usage: python game.py numGames"
	exit(0)

game = Game(100, 0)
game.linkPlayer(0, SGDAI())
game.linkPlayer(1, RationalAI())

count = [0, 0]
roundlengths = []
history = []
chipsHist = []
for i in range(int(sys.argv[1])):
	p2wins = game.playGame()
	count[p2wins] += 1
	if p2wins:
		history.append("W")
	else:
		history.append("L")
	roundlengths.append(game.roundNum)
	chipsHist.append(game.chipsHist)
	game.newGame()
print " "
print "Final Tally: ", count
print "Round Lengths: ", roundlengths
print history
for lst in chipsHist:
	print lst