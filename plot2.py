import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

player = [100, 101, 99, 100, 106, 104, 103, 104, 116, 116, 114, 115, 117, 112, 110, 111, 105, 99, 101, 102, 104, 105, 104, 105, 90, 91, 89, 90, 102, 103, 105, 106, 111, 112, 117, 111, 113, 158, 163, 200]
#player = [100, 114, 126, 124, 123, 124, 123, 125, 124, 122, 124, 129, 131, 129, 141, 139, 78, 83, 82, 80, 79, 158, 116, 117, 116, 122, 124, 160, 159, 147, 118, 116, 118, 120, 200]
#player = [100, 101, 119, 120, 40, 80, 79, 80, 160, 161, 122, 123, 125, 126, 128, 129, 131, 132, 150, 100, 112, 113, 26, 52, 0]


opp = [200 - i for i in player]
x = range(len(player))

red_patch = mpatches.Patch(color='r', label='SGDAI')
green_patch = mpatches.Patch(color='b', label='RationalAI')
plt.legend(handles=[red_patch, green_patch])

plt.title('SGDAI vs. RationalAI')
plt.ylabel('Total Chips')
plt.xlabel('Round Number')

plt.plot(x, player, 'r-o', x, opp, 'b-o') #, x, FA, 'g-o')
plt.axis([0, len(player), 0, 200])
plt.show()

