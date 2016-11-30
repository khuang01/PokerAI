from Poker import *

# cards = [(1,3), (3,4), (1, 7)]
# IDs = cardsToID(cards)
# print evaluatePile(IDs)

# newGame = Game(2)

# gui = ["QC", "2C", "KC", "8S", "KS", "TD", "8H"]
# cards = GUIToCards(gui)
# IDs = cardsToID(cards)

# gui1 = ["KD", "KC", "4D", "6C", "7C", "QS", "8H"]
# cards = GUIToCards(gui1)
# IDs = cardsToID(cards)
# e1 = evaluatePile(IDs)

# gui2 = ["5S", "TD", "4D", "6C", "7C", "QS", "8H"]
# cards = GUIToCards(gui2)
# IDs = cardsToID(cards)
# e2 = evaluatePile(IDs)

# gui1 = ["9S", "JH"]
# cards = GUIToCards(gui1)
# p1 = cardsToID(cards)
# gui2 = ["7S", "8D"]
# cards = GUIToCards(gui2)
# p2 = cardsToID(cards)
# gui3 = ["9C", "7H", "3C", "KC", "KH"]
# cards = GUIToCards(gui3)
# board = cardsToID(cards)
# newGame.board[0] = board[0]
# newGame.board[1] = board[1]
# newGame.board[2] = board[2]
# newGame.board[3] = board[3]
# newGame.board[4] = board[4]
# newGame.revealedCards = 0
# begin = time.time()
# wins, ties = newGame.simulateGames(p1, p2, 10000)
# print "Player 1: ", gui1
# print "Player 2: ", gui2
# print "Board: ", gui3
# print "Wins: ", float(wins) / 10000, "Tie: ", float(ties) / 10000
# print "Time taken: ", time.time() - begin


#####################################################################

# newGame = Game(2)
# print handToGUI(newGame.board)
# # print newGame.playerCards
# # print newGame.getPlayerCards(0)
# p1 = Player(newGame, 0)
# print "Player1: ", handToGUI(p1.cards)
# print "P1 Standard Probability: ", p1.standardProb
# p2 = Player(newGame, 1)
# print "Player2: ", handToGUI(p2.cards)
# print "P2 Standard Probability: ", p2.standardProb
# print "Preflop: ", newGame.p1Wins, newGame.tie, newGame.p2Wins
# newGame.flop()
# p1.refreshStandardProb()
# p2.refreshStandardProb()
# print "P1 Standard Probability: ", p1.standardProb
# print "P2 Standard Probability: ", p2.standardProb
# print "Flop: ", newGame.p1Wins, newGame.tie, newGame.p2Wins
# newGame.turn()
# p1.refreshStandardProb()
# p2.refreshStandardProb()
# print "P1 Standard Probability: ", p1.standardProb
# print "P2 Standard Probability: ", p2.standardProb
# print "Turn: ", newGame.p1Wins, newGame.tie, newGame.p2Wins
# newGame.river()
# p1.refreshStandardProb()
# p2.refreshStandardProb()
# print "P1 Standard Probability: ", p1.standardProb
# print "P2 Standard Probability: ", p2.standardProb
# print "River: ", newGame.p1Wins, newGame.tie, newGame.p2Wins

#####################################################################

# newGame = Game(2)
# p1 = RandomAI(newGame, 0)
# print p1.action()
# p2 = RationalAI(newGame, 1)

newGame = Game(2, 100, 0)
p1 = RandomAI(newGame, 0)
p2 = RationalAI(newGame, 1)
newGame.blinds()
print newGame.totalChips



