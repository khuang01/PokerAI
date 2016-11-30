import numpy as np
import random
import time

def IDtoCard(id):
	# (value, suit)
	return (id / 4 + 2, id % 4)

def handtoCards(hand):
	return [(id / 4 + 2, id % 4) for id in hand]

def checkEqual(iterator):
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == rest for rest in iterator)

def cardsToGUI(lst):
	suits = ['D','C','H','S']
	values = ["-1","-1","2","3","4","5","6","7","8","9","T","J","Q","K","A"]
	return [values[i[0]] + suits[i[1]] for i in lst]

def cardToID((value, suit)):
	return (value - 2) * 4 + suit

def cardsToID(lst):
	return [cardToID(i) for i in lst]

def handToGUI(hand):
	return cardsToGUI(handtoCards(hand))

# 0: junk, 1: pair, 2: two pair, 3: triple, 4: straight, 5: flush
# 6: full house, 7: quad, 8: straight flush
def evaluatePile(pile):
	cards = sorted([(id / 4 + 2, id % 4) for id in pile])
	valCount = [0 for i in range(15)]
	suitCount = [0 for i in range(4)]
	for card in cards:
		valCount[card[0]] += 1
		suitCount[card[1]] += 1
	straightHigh = 0
	curStraight = 0
	if valCount[14]:
		curStraight = 1
	quads = 0
	triple = 0
	pair1 = 0
	pair2 = 0
	flush = -1
	for i in range(2, 15):
		if valCount[i]:
			curStraight += 1
			if curStraight >= 5:
				straightHigh = i
			if valCount[i] == 4:
				quads = i
			if valCount[i] == 3:
				pair1 = max(pair1, triple)
				triple = i
			if valCount[i] == 2:
				pair2 = pair1
				pair1 = i
		else:
			curStraight = 0
	for i in range(4):
		if suitCount[i] >= 5:
			flush = i
			break
	if straightHigh and flush != -1:
		best = 0
		cur = 0
		length = 0
		if ((14, flush) in cards):
			cur = 1
			length = 1
		for card in cards:
			if card[1] != flush:
				continue
			if card[0] == cur + 1:
				cur = card[0]
				length += 1
				if length >= 5:
					best = cur
			else:
				length = 1
			cur = card[0]
		if best:
			return (8, best, 0, 0, 0, 0)
	if quads:
		lastCard = 0
		for card in reversed(cards):
			if card[0] != quads:
				lastCard = card[0]
				break
		return (7, quads, lastCard, 0, 0, 0)
	if triple and pair1:
		return (6, triple, pair1, 0, 0, 0)
	if flush != -1:
		result = [0, 0, 0, 0, 0]
		index = 0
		for card in reversed(cards):
			if card[1] == flush:
				result[index] = card[0]
				index += 1
				if index == 5:
					break
		return (5, result[0], result[1], result[2], result[3], result[4])
	if straightHigh:
		return (4, straightHigh, 0, 0, 0, 0)
	if triple:
		card1, card2 = 0, 0
		for card in reversed(cards):
			if card[0] != triple:
				if card1:
					card2 = card[0]
					break
				card1 = card[0]
		return (3, triple, card1, card2, 0, 0)
	if pair1 and pair2:
		lastCard = 0
		for card in reversed(cards):
			if card[0] != pair1 and card[0] != pair2:
				lastCard = card[0]
				break
		return (2, pair1, pair2, lastCard, 0, 0)
	if pair1:
		result = [0, 0, 0]
		index = 0
		for card in reversed(cards):
			if card[0] != pair1:
				result[index] = card[0]
				index += 1
				if index == 3:
					break
		return (1, pair1, result[0], result[1], result[2], 0)
	# junk
	return (0, cards[-1][0], cards[-2][0], cards[-3][0], cards[-4][0], cards[-5][0])

def GUIToCards(lst):
	conv = {}
	conv['D'] = 0
	conv['C'] = 1
	conv['H'] = 2
	conv['S'] = 3
	result = []
	for gui in lst:
		if gui[0] == 'T':
			value = 10
		elif gui[0] == 'J':
			value = 11
		elif gui[0] == 'Q':
			value = 12
		elif gui[0] == 'K':
			value = 13
		elif gui[0] == 'A':
			value = 14
		else:
			value = int(gui[0])
		result.append((value, conv[gui[1]]))
	return result



class Game:
	def __init__(self, numPlayers, startingChips, bigBlind):
		self.bigBlind = bigBlind
		self.bettingRound = 0
		self.pot = 0
		self.curRaise = 0
		self.playerRaise = 0
		self.cards = [False for i in range(52)]
		self.board = [-1 for i in range(5)]
		self.gameOver = False
		# -1 if tie
		self.roundWinner = 0
		for i in range(5):
			card = random.randint(0,51)
			while (self.cards[card]):
				card = random.randint(0,51)
			self.cards[card] = True
			self.board[i] = card
		self.playerCards = [-1 for i in range(2 * numPlayers)]
		self.totalChips = [startingChips for i in range(numPlayers)]
		self.allIn = [False for i in range(numPlayers)]
		for i in range(2 * numPlayers):
			card = random.randint(0,51)
			while (self.cards[card]):
				card = random.randint(0,51)
			self.cards[card] = True
			self.playerCards[i] = card
		self.revealedCards = 0
		self.p1Wins, self.tie, self.p2Wins = self.simulateGames(self.getPlayerCards(0), self.getPlayerCards(1), 10000)
		
	def restart(self):
		self.bigBlind = 1 - self.bigBlind
		self.cards = [False for i in range(52)]
		for i in range(5):
			card = random.randint(0,51)
			while (self.cards[card]):
				card = random.randint(0,51)
			self.cards[card] = True
			self.board[i] = card
		self.allIn = [False for i in range(numPlayers)]
		for i in range(2 * numPlayers):
			card = random.randint(0,51)
			while (self.cards[card]):
				card = random.randint(0,51)
			self.cards[card] = True
			self.playerCards[i] = card
		self.revealedCards = 0
		self.p1Wins, self.tie, self.p2Wins = self.simulateGames(self.getPlayerCards(0), self.getPlayerCards(1), 10000)

	def blinds(self):
		smallBlind = 1 - self.bigBlind
		big = min(2, self.totalChips[self.bigBlind], self.totalChips[smallBlind])
		self.pot += big
		self.totalChips[self.bigBlind] -= big
		small = min(1, self.totalChips[self.bigBlind], self.totalChips[smallBlind])
		self.pot += small
		self.totalChips[smallBlind] -= small
		self.curRaise = big - small
		self.playerRaise = self.bigBlind

	def getPlayerCards(self, player):
		return (self.playerCards[2 * player], self.playerCards[2 * player + 1])

	def flop(self):
		self.revealedCards = 3
		self.p1Wins, self.tie, self.p2Wins = self.simulateGames(self.getPlayerCards(0), self.getPlayerCards(1), 10000)
		self.bettingRound = 0

	def turn(self):
		self.revealedCards = 4
		self.p1Wins, self.tie, self.p2Wins = self.simulateGames(self.getPlayerCards(0), self.getPlayerCards(1), 10000)
		self.bettingRound = 0

	def river(self):
		self.revealedCards = 5
		self.p1Wins, self.tie, self.p2Wins = self.simulateGames(self.getPlayerCards(0), self.getPlayerCards(1), 10000)
		self.bettingRound = 0
		if self.p1Wins > .99:
			self.roundWinner = 0
		elif self.tie > .99:
			self.roundWinner = -1
		else:
			self.roundWinner = 1

	def giveBack(self, playerNum, amt):
		self.pot -= amt
		self.totalChips[playerNum] += amt

	# returns False -> checks/calls, True -> raises,
	def pushChips(self, playerNum, amt):
		assert amt >= self.curRaise, "Not enough chips to call/raise"
		amt = min(amt, self.totalChips[playerNum])
		if amt > self.curRaise:
			self.curRaise = amt - self.curRaise
			self.playerRaise = playerNum
			result = True
		else:
			self.curRaise = 0
			result = False
			self.giveBack(1 - playerNum, self.curRaise - amt)
		self.pot += amt
		self.totalChips[playerNum] -= amt
		if self.totalChips[playerNum] == 0:
			self.allIn[playerNum] = True
		return result

	def distributeChips(self):
		if self.roundWinner == -1:
			self.totalChips[0] += self.pot / 2
			self.totalChips[1] += self.pot / 2
		else:
			self.totalChips[self.roundWinner] += self.pot
		self.pot = 0
		self.curRaise = 0
		for i in range(self.numPlayers):
			if self.totalChips[i] == 0:
				self.gameOver = True
			else:
				self.allIn[i] = False

	def simulateGames(self, player1, player2, n=10000):
		simulationBoard = [-1 for i in range(7)]
		for i in range(5):
			simulationBoard[i] = self.board[i]
		allCards = [False for i in range(52)]
		for i in range(self.revealedCards):
			allCards[self.board[i]] = True
		for i in player1:
			allCards[i] = True
		for i in player2:
			allCards[i] = True
		total1 = 0
		tie = 0
		if self.revealedCards == 5:
			simulationBoard[5] = player1[0]
			simulationBoard[6] = player1[1]
			e1 = evaluatePile(simulationBoard)
			simulationBoard[5] = player2[0]
			simulationBoard[6] = player2[1]
			e2 = evaluatePile(simulationBoard)
			p1Wins = 0.
			tie = 0.
			if e1 > e2:
				p1Wins = 1.
			elif e1 == e2:
				tie = 1.
			p2Wins = 1. - p1Wins - tie
			return (p1Wins, tie, p2Wins)
		for game in range(n):
			for i in range(self.revealedCards, 5):
				card = random.randint(0,51)
				while (allCards[card]):
					card = random.randint(0,51)
				simulationBoard[i] = card
				allCards[card] = True
			simulationBoard[5] = player1[0]
			simulationBoard[6] = player1[1]
			e1 = evaluatePile(simulationBoard)
			simulationBoard[5] = player2[0]
			simulationBoard[6] = player2[1]
			e2 = evaluatePile(simulationBoard)
			if e1 > e2:
				total1 += 1
			elif e1 == e2:
				tie += 1
			for i in range(self.revealedCards, 5):
				allCards[simulationBoard[i]] = False
		p1Wins = float(total1) / n
		tie = float(tie) / n
		p2Wins = 1. - p1Wins - tie
		return (p1Wins, tie, p2Wins)

	def standardProb(self, player, n=100):
		allCards = [False for i in range(52)]
		for i in range(self.revealedCards):
			allCards[self.board[i]] = True
		for i in player:
			allCards[i] = True
		count = 0
		total = 0
		for i in range(51):
			for j in range(i + 1, 52):
				if allCards[i] or allCards[j]:
					continue
				p1Wins, tie, p2Wins = self.simulateGames(player, (i, j), n)
				if p1Wins + .5 * tie > 0.5:
					count += 1
				total += 1
		return float(count) / total
	

class Player(object):
	def __init__(self, game, playerNum):
		self.game = game
		self.playerNum = playerNum
		self.cards = game.getPlayerCards(playerNum)
		self.standardProb = 0.
		# self.standardProb = self.game.standardProb(self.cards)
		self.revealedCards = 0

	# def linkGame(self, game):
	# 	self.game = game

	def refreshRevealedCards(self):
		self.revealedCards = game.revealedCards

	def refreshCards(self):
		self.cards = game.getPlayerCards(self.playerNum)

	def refreshStandardProb(self, n=100):
		self.standardProb = self.game.standardProb(self.cards, n)

	def action(self):
		pass

class RandomAI(Player):
	def action(self):
		result = random.randint(-1,1)
		if (result == 1):
			return self.game.curRaise + max(self.game.pot, self.game.curRaise)
		elif (result == 0 or self.game.curRaise == 0):
			return self.game.curRaise
		else:
			return -1
	# filler function; RandomAI has no use for standardProb
	def refreshStandardProb(self, n=100):
		self.standardProb = 0

class RationalAI(Player):
	# def __init__(self, game, playerNum, c, r):
	# 	super(RationalAI, self).__init__(game, playerNum):
	# 	self.c = c
	# 	self.r = r
	def action(self):
		if self.standardProb > .9:
			return self.game.curRaise + max(self.game.pot, self.game.curRaise)
		elif self.standardProb > .5:
			return self.game.curRaise
		elif self.game.curRaise:
			return -1
		else:
			return 0

class AlwaysCallAI(Player):
	def action(self):
		return self.game.curRaise
	# filler function; AlwaysCallAI has no use for standardProb
	def refreshStandardProb(self, n=100):
		self.standardProb = 0

# class AgressiveAI(Player):


# newGame = Game(2)
# begin = time.time()
# for i in range(50 ** 3):
# 	x = newGame.evaluatePile([1,2,3,4,0,5,6])
# print time.time() - begin
# print newGame.flush([3,7,11,15,18])