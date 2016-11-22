from Poker import *

# cards = [(1,3), (3,4), (1, 7)]
# IDs = cardsToID(cards)
# print evaluatePile(IDs)

newGame = Game(2)

gui = ["QC", "2C", "KC", "8S", "KS", "TD", "8H"]
cards = GUIToCards(gui)
IDs = cardsToID(cards)

gui1 = ["KD", "KC", "4D", "6C", "7C", "QS", "8H"]
cards = GUIToCards(gui1)
IDs = cardsToID(cards)
e1 = evaluatePile(IDs)

gui2 = ["5S", "TD", "4D", "6C", "7C", "QS", "8H"]
cards = GUIToCards(gui2)
IDs = cardsToID(cards)
e2 = evaluatePile(IDs)

gui1 = ["TC", "TD"]
cards = GUIToCards(gui1)
p1 = cardsToID(cards)
gui2 = ["3C", "2D"]
cards = GUIToCards(gui2)
p2 = cardsToID(cards)
gui3 = ["AS", "JH", "3H"]
cards = GUIToCards(gui3)
board = cardsToID(cards)
# newGame.board[0] = board[0]
# newGame.board[1] = board[1]
# newGame.board[2] = board[2]
# newGame.revealedCards = 3
begin = time.time()
wins, ties = newGame.simulateGames(p1, p2, 10000)
print float(wins) / 10000, float(ties) / 10000
print "Time taken: ", time.time() - begin

begin = time.time()
wins, count = newGame.standardProb(p1, 101)
print float (wins) / count
print "Time taken: ", time.time() - begin

# print cards[-1][1]
# print cardToID((3,2))
# IDs = cardsToID([(4,1), (11,2), (13, 0)])
# print cardsToGUI([(4,1), (11,2), (13, 0)])
# for i in IDs:
# 	print IDtoCard(i)