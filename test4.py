from Poker import *
import time

game = Game(2, 100, 0)
game.linkPlayer(0, RationalAI())
game.linkPlayer(1, SGDAI())
game.pot = 3
game.curRaise = 1
game.players[1].standardProbEst = .17
print game.players[1].action()