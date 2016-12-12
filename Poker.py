import numpy as np
import random
import time

def numCardsToStage(revealedCards):
	if revealedCards == 0:
		return 0
	else:
		return revealedCards - 2

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

class Game:
	def __init__(self, startingChips, bigBlind):
		self.numPlayers = 2
		self.players = [None for i in range(self.numPlayers)]
		self.bigBlind = bigBlind
		self.bettingRound = 0
		self.totalPush = 0
		self.pot = 0
		self.curRaise = 0
		self.playerRaise = 0
		self.cards = [False for i in range(52)]
		self.board = [-1 for i in range(5)]
		self.gameOver = False
		self.roundOver = False
		self.startPlayer = 1 - bigBlind
		self.omniscientProb = [[-1.,-1.,-1.,-1.], [-1.,-1.,-1.,-1.]]
		self.numRaises = [0, 0]
		self.chipsHist = []
		# -1 if tie
		self.roundWinner = -1
		self.human = False
		for i in range(5):
			card = random.randint(0,51)
			while (self.cards[card]):
				card = random.randint(0,51)
			self.cards[card] = True
			self.board[i] = card
		self.playerCards = [-1 for i in range(2 * self.numPlayers)]
		self.startingChips = startingChips
		self.totalChips = [startingChips for i in range(self.numPlayers)]
		self.allIn = [False for i in range(self.numPlayers)]
		for i in range(2 * self.numPlayers):
			card = random.randint(0,51)
			while (self.cards[card]):
				card = random.randint(0,51)
			self.cards[card] = True
			self.playerCards[i] = card
		self.revealedCards = 0
		self.p1Wins, self.tie, self.p2Wins = self.MonteCarlo(self.getPlayerCards(0), self.getPlayerCards(1), 10000)
		self.updateOmniscient(0)
	
	def linkPlayer(self, playerNum, player):
		self.players[playerNum] = player
		player.game = self
		player.playerNum = playerNum
		player.installHuman()
		player.refreshCards()

	def printBoard(self):
		currentBoard = []
		for i in range(self.revealedCards):
			currentBoard.append(self.board[i])
		print "Board: ", handToGUI(currentBoard)

	def newGame(self):
		self.gameOver = False
		self.totalChips = [self.startingChips for i in range(self.numPlayers)]
		self.chipsHist = []

	def playGame(self):
		self.roundNum = 0
		while not self.gameOver:
			print "Round Number: ", self.roundNum
			self.roundNum += 1
			# print handToGUI(self.board)
			if not self.human:
				print handToGUI(self.getPlayerCards(0))
				print handToGUI(self.getPlayerCards(1))
			self.playRound()
			self.printCurrentState()
			self.redeal()
			self.chipsHist.append(self.totalChips[1])
		if self.totalChips[0]:
			return 0
		else:
			return 1

	def playRound(self):
		print "PREFLOP"
		self.blinds()
		for player in self.players:
			player.preflop()
		self.playStage()
		if not self.roundOver:
			print "FLOP"
			self.flop()
			self.printBoard()
			self.playStage()
		if not self.roundOver:
			print "TURN"
			self.turn()
			self.printBoard()
			self.playStage()
		if not self.roundOver:
			print "RIVER"
			self.river()
			self.printBoard()
			self.playStage()
		if not self.human:
			print "Omniscient: ", self.omniscientProb
		for player in self.players:
			player.updateParameters()
		self.distributeChips()

	def playStage(self):
		curPlayer = self.startPlayer
		for player in self.players:
			player.refreshStandardProbEst(.25)
			player.refreshR()
		# print "Standard prob: ", p[1].standardProb
		# print "Standard prob est: ", self.players[1].standardProbEst
		self.bettingRound = 0
		cc = 0
		while (cc < 2):
			push = min(self.players[curPlayer].action(), self.curRaise + self.totalChips[1 - curPlayer])
			if push == -1:
				self.roundWinner = 1 - curPlayer
				self.roundOver = True
				break
			if not self.human:
				print "curPlayer: ", curPlayer, "curRaise: ", self.curRaise, "curPot: ", self.pot, "Push: ", push
			if min(self.totalChips[curPlayer], push) == self.curRaise:
				cc += 1
			else:
				cc = 1
			if (self.pushChips(curPlayer, push)):
				self.numRaises[curPlayer] += 1
			curPlayer = 1 - curPlayer
			self.bettingRound += 1
			self.totalPush += 1
		print "Pot: ", self.pot, "Totalchips: ", self.totalChips

	def redeal(self):
		self.roundOver = False
		self.roundWinner = -1
		self.bigBlind = 1 - self.bigBlind
		self.startPlayer = 1 - self.startPlayer
		for i in range(52):
			self.cards[i] = False
		for i in range(5):
			card = random.randint(0,51)
			while (self.cards[card]):
				card = random.randint(0,51)
			self.cards[card] = True
			self.board[i] = card
		for i in range(2 * self.numPlayers):
			card = random.randint(0,51)
			while (self.cards[card]):
				card = random.randint(0,51)
			self.cards[card] = True
			self.playerCards[i] = card
		for i in range(self.numPlayers):
			self.players[i].refreshCards()
			self.allIn[i] = False
		self.revealedCards = 0
		self.totalPush = 0
		self.p1Wins, self.tie, self.p2Wins = self.MonteCarlo(self.getPlayerCards(0), self.getPlayerCards(1), 10000)
		for i in range(4):
			self.omniscientProb[0][i] = -1.
			self.omniscientProb[1][i] = -1.
		self.updateOmniscient(0)
		self.numRaises[0] = 0
		self.numRaises[1] = 0

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
		self.p1Wins, self.tie, self.p2Wins = self.MonteCarlo(self.getPlayerCards(0), self.getPlayerCards(1), 10000)
		self.updateOmniscient(1)

	def turn(self):
		self.revealedCards = 4
		self.p1Wins, self.tie, self.p2Wins = self.MonteCarlo(self.getPlayerCards(0), self.getPlayerCards(1), 10000)
		self.updateOmniscient(2)

	def river(self):
		self.revealedCards = 5
		self.p1Wins, self.tie, self.p2Wins = self.MonteCarlo(self.getPlayerCards(0), self.getPlayerCards(1), 10000)
		self.updateOmniscient(3)
		if self.p1Wins > .99:
			self.roundWinner = 0
		elif self.tie > .99:
			self.roundWinner = -1
		else:
			self.roundWinner = 1

	def giveBack(self, playerNum, amt):
		self.pot -= amt
		self.totalChips[playerNum] += amt

	# returns False -> checks/calls, True -> raises
	# pushChips takes in the amt that the player desires to push,
	# and then reduces it down if player does not have enough
	def pushChips(self, playerNum, amt):
		assert amt >= self.curRaise, "Not enough chips to call/raise"
		# no 4-bets
		if self.bettingRound == 3:
			amt = self.curRaise
		amt = min(amt, self.totalChips[playerNum])
		if amt > self.curRaise:
			self.curRaise = amt - self.curRaise
			self.playerRaise = playerNum
			result = True
		else:
			result = False
			self.giveBack(1 - playerNum, self.curRaise - amt)
			self.curRaise = 0
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

	def MonteCarlo(self, player1, player2, n=10000):
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
				p1Wins, tie, p2Wins = self.MonteCarlo(player, (i, j), n)
				if p1Wins + .5 * tie > 0.5:
					count += 1
				total += 1
		return float(count) / total

	def standardProbEst(self, player, p, n=100):
		allCards = [False for i in range(52)]
		for i in range(self.revealedCards):
			allCards[self.board[i]] = True
		for i in player:
			allCards[i] = True
		count = 0
		total = 0
		for i in range(51):
			for j in range(i + 1, 52):
				if allCards[i] or allCards[j] or random.random() > p:
					continue
				p1Wins, tie, p2Wins = self.MonteCarlo(player, (i, j), n)
				if p1Wins + .5 * tie > 0.5:
					count += 1
				total += 1
		return float(count) / total
	
	def printCurrentState(self):
		print "Total Chips: ", self.totalChips
		print "Big Blind: ", self.bigBlind
		print " "

	def updateOmniscient(self, i):
		self.omniscientProb[0][i] = self.p1Wins + .5 * self.tie
		self.omniscientProb[1][i] = self.p2Wins + .5 * self.tie

class Player(object):
	def __init__(self):
		self.game = None
		self.playerNum = -1
		self.cards = (-1, -1)#game.getPlayerCards(playerNum)
		self.standardProb = 0.
		self.standardProbEst = 0.
		self.revealedCards = 0
		self.R = [0,0,0,0]

	def installHuman(self):
		pass

	def preflop(self):
		pass

	def refreshR(self):
		stage = numCardsToStage(self.game.revealedCards)
		# self.R[stage] = (self.game.totalPush + 1) / 2 - stage
		self.R[stage] = self.game.numRaises[1 - self.playerNum]

	def refreshRevealedCards(self):
		self.revealedCards = self.game.revealedCards

	def refreshCards(self):
		self.cards = self.game.getPlayerCards(self.playerNum)

	def refreshStandardProb(self, n=100):
		self.standardProb = self.game.standardProb(self.cards, n)

	def refreshStandardProbEst(self, p, n=100):
		self.standardProbEst = self.game.standardProbEst(self.cards, p, n)

	def action(self):
		pass

	def updateParameters(self):
		pass

class RandomAI(Player):
	def action(self):
		result = random.randint(-1,1)
		if (result == 1):
			return self.game.curRaise + self.game.pot
		elif (result == 0 or self.game.curRaise == 0):
			return self.game.curRaise
		else:
			return -1
	# filler function; RandomAI has no use for standardProb
	def refreshStandardProb(self, n=100):
		pass
	def refreshStandardProbEst(self, p, n=100):
		pass

class AggressiveAI(Player):
	def action(self):
		return self.game.curRaise + self.game.pot
	# filler function; AlwaysCallAI has no use for standardProb
	def refreshStandardProb(self, n=100):
		pass
	def refreshStandardProbEst(self, p, n=100):
		pass

class AlwaysCallAI(Player):
	def action(self):
		return self.game.curRaise
	# filler function; AlwaysCallAI has no use for standardProb
	def refreshStandardProb(self, n=100):
		pass
	def refreshStandardProbEst(self, p, n=100):
		pass

class RationalAI(Player):
	def __init__(self, c=.5, r=.8):
		super(RationalAI, self).__init__()
		self.c = c
		self.r = r
	def action(self):
		if self.standardProbEst > self.c:
			return self.game.curRaise + self.game.pot
		elif self.standardProbEst > self.r:
			return self.game.curRaise
		elif self.game.curRaise:
			return -1
		else:
			return 0

class PotAI(Player):
	def __init__(self, m=1., a=1., b=0., eta=.05):
		super(PotAI, self).__init__()
		self.m = m
		self.a = a
		self.b = b
		self.eta = eta
		self.estP = 0.
		self.allP = [0., 0., 0., 0.]
		
	def action(self):
		p = self.standardProbEst
		B = self.game.curRaise
		C = self.game.pot
		# p *= .6
		# print p
		if p > .8:
			return self.game.curRaise + self.game.pot
		# A = (p * C - (1 - p) * B) / (1 - 2 * p)
		A = (p * C - (1 - p) * B)
		if (A < 0):
			return -1
		else:
			return self.game.curRaise

class QLearningAI(Player):
	def __init__(self, alpha=.05, gamma=1., epsilon=.05):
		super(QLearningAI, self).__init__()
		self.alpha = alpha
		self.gamma = gamma
		self.epsilon = epsilon
		self.Q = [[-.1, 0., 0.] for i in range(200)]
		self.stateActionPairs = []

	def pBucket(self, p):
		if p < .3:
			return 0
		elif p < .6:
			return 1
		elif p < .8:
			return 2
		elif p < .9:
			return 3
		else:
			return 4

	def calculateState(self):
		stage = numCardsToStage(self.game.revealedCards)
		r = 0
		if self.game.numRaises[1 - self.playerNum]:
			r = 1
		pHat = self.standardProbEst
		potOdds = float(self.game.curRaise) / (self.game.curRaise + self.game.pot)
		return stage + 4 * (r + 2 * (self.pBucket(pHat) + 5 * self.pBucket(potOdds)))
		
	def action(self):
		s = self.calculateState()
		a = 0
		if (random.random() < self.epsilon):
			a = random.randint(0, 2)
		else:
			value = self.Q[s][0]
			if value < self.Q[s][1]:
				a = 1
				value = self.Q[s][1]
			if value < self.Q[s][2]:
				a = 2
				value = self.Q[s][2]
		self.stateActionPairs.append((s,a))
		if a == 0:
			if not self.game.curRaise:
				return 0
			return -1
		elif a == 1:
			return self.game.curRaise
		else:
			return self.game.curRaise + self.game.pot

	def updateParameters(self):
		if not len(self.stateActionPairs):
			return
		lastPair = self.stateActionPairs[-1]
		if self.game.roundWinner == self.playerNum:
			reward = (self.game.pot - self.game.curRaise) / 2
		else:
			reward = (self.game.curRaise - self.game.pot) / 2
		self.Q[lastPair[0]][lastPair[1]] *= 1. - self.alpha
		self.Q[lastPair[0]][lastPair[1]] += self.alpha * reward
		length = len(self.stateActionPairs)
		for i in range(length - 2, -1, -1):
			sc = self.stateActionPairs[i][0]
			ac = self.stateActionPairs[i][1]
			sn = self.stateActionPairs[i + 1][0]
			an = self.stateActionPairs[i + 1][1]
			self.Q[sc][ac] *= 1. - self.alpha
			self.Q[sc][ac] += self.alpha * self.gamma * self.Q[sn][an]

		self.stateActionPairs = []

class SGDAI(Player):
	def __init__(self, m=.8, a=0.7728, b=.013, eta=.03):
		super(SGDAI, self).__init__()
		self.m = m
		self.a = a
		self.b = b
		self.eta = eta
		self.estP = [0., 0., 0., 0.]
		self.refinedP = [0., 0., 0., 0.]
		self.R = [0, 0, 0, 0]
		
	def action(self):
		stage = numCardsToStage(self.game.revealedCards)
		if stage == 0:
			assert self.R[stage] == 0, "r[0] not 0"
		self.estP[stage] = self.standardProbEst

		p = self.standardProbEst
		p = self.m ** self.game.numRaises[1 - self.playerNum] * (self.a * p + self.b)
		
		self.refinedP[stage] = p
		# print "Stage: ", stage, "Estimated p: ", p
		if p > .65:
			return self.game.curRaise + self.game.pot

		B = self.game.curRaise
		C = self.game.pot
		# A = (p * C - (1 - p) * B) / (1 - 2 * p)
		A = (p * C - (1 - p) * B)
		if (A < 0):
			return -1
		else:
			return self.game.curRaise

	def updateParameters(self):
		opponentCards = self.game.getPlayerCards(1 - self.playerNum)
		for stage in range(1, numCardsToStage(self.game.revealedCards)):
			# print "Stage: ", stage
			diffP = self.refinedP[stage] - self.game.omniscientProb[self.playerNum][stage]
			self.a -= self.eta * 2 * diffP * self.m ** self.R[stage + 1] * self.estP[stage]
			self.b -= self.eta * 2 * diffP * self.m ** self.R[stage + 1]
			self.m -= self.eta * diffP * self.R[stage + 1] * self.refinedP[stage] / self.m
			self.m = min(.9, max(self.m, .6))
		# print "a: ", self.a, "b: ", self.b, "m: ", self.m

class Human(Player):
	# def __init__(self):
	# 	super(Human, self).__init__()
	# 	self.game.human = True
	def installHuman(self):
		self.game.human = True

	def preflop(self):
		if self.playerNum == self.game.bigBlind:
			print "You are big blind"
		else:
			print "You are small blind"
		print "Your cards: ", handToGUI(self.game.getPlayerCards(self.playerNum))

	def action(self):
		print "Current pot: ", self.game.pot, "Opponent has raised: ", self.game.curRaise
		result = raw_input("Fold (f), check/call (c), raise (r): ")
		while result != 'f' and result != 'c' and result != 'r':
			result = raw_input("Fold (f), check/call (c), raise (r): ")
		if result == 'c':
			return self.game.curRaise
		elif result == 'f':
			return -1
		else:
			while True:
				try:
					amt = int(raw_input("Raise amount: "))
					break
				except ValueError:
					print("Raise amount: ")
			return self.game.curRaise + amt

	def refreshStandardProb(self, n=100):
		pass

	def refreshStandardProbEst(self, p, n=100):
		pass
