from Poker import *
import time

# game = Game(2, 100, 0)
# game.linkPlayer(0, RandomAI(game, 0))
# game.linkPlayer(1, RationalAI(game, 1))

# count = [0, 0]
# roundlengths = []
# for i in range(10):
# 	count[game.playGame()] += 1
# 	roundlengths.append(game.roundNum)
# 	game.newGame()
# print " "
# print "Final Tally: ", count
# print "Round Lengths: ", roundlengths

gui1 = ["2C", "JS", "KS", "5D", "KC"]
cards = GUIToCards(gui1)
IDs = cardsToID(cards)


game = Game(2, 100, 0)
game.board = IDs
game.revealedCards = 4
# game.linkPlayer(1, RationalAI(game, 1))
# game.playerCards[2] = 1
# game.playerCards[3] = 48

cards = cardsToID(GUIToCards(["QS", "TS"]))
begin = time.time()
print game.standardProbEst(cards)
print "Time: ", time.time() - begin