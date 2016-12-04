import matplotlib.pyplot as plt

player = [100, 101, 99, 100, 106, 104, 103, 104, 116, 116, 114, 115, 117, 112, 110, 111, 105, 99, 101, 102, 104, 105, 104, 105, 90, 91, 89, 90, 102, 103, 105, 106, 111, 112, 117, 111, 113, 158, 163, 200]
opp = [200 - i for i in player]
x = range(len(player))

plt.plot(x, player, 'r-o', x, opp, 'b-o') #, x, FA, 'g-o')
plt.axis([0, len(player), 0, 200])
plt.show()

