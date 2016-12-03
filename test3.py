from Poker import *
import time

game = Game(2, 100, 0)
game.linkPlayer(0, RationalAI())
game.linkPlayer(1, SGDAI())
# game.linkPlayer(1, SGDAI())

count = [0, 0]
roundlengths = []
history = []
for i in range(30):
	p2wins = game.playGame()
	count[p2wins] += 1
	if p2wins:
		history.append("W")
	else:
		history.append("L")
	roundlengths.append(game.roundNum)
	game.newGame()
print " "
print "Final Tally: ", count
print "Round Lengths: ", roundlengths
print history

# gui1 = ["2C", "JS", "KS", "5D", "KC"]
# cards = GUIToCards(gui1)
# IDs = cardsToID(cards)


# game = Game(2, 100, 0)
# game.board = IDs
# game.revealedCards = 4

# cards = cardsToID(GUIToCards(["QS", "TS"]))
# begin = time.time()
# print game.standardProbEst(cards)
# print "Time: ", time.time() - begin